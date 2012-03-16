"""mockfs: A simple mock filesystem for unit tests."""

import os
import copy
import errno

from mockfs import util


def _OSError(err, path):
    """Return an OSError with an appropriate error string"""
    return OSError(err, os.strerror(err) + ": '%s'" % path)


class MockFS(object):
    """
    MockFS implementation object

    Provides stubs for functions in :mod:`os`, :mod:`os.path`, and :mod:`glob`.

    """

    def __init__(self, entries=None):
        self._entries = {}
        self.add_entries(entries)

    def add_entries(self, entries):
        """Add new entries to mockfs."""
        new_entries = util.build_nested_dict(entries)
        util.merge_dicts(new_entries, self._entries)

    def exists(self, path):
        """
        Return True if path exists

        Implements the :func:`os.path.exists` interface.

        """
        path = util.sanitize(path)
        dirent = self._direntry(os.path.dirname(path))
        if path == '/':
            return bool(dirent)
        return bool(dirent) and os.path.basename(path) in dirent

    def isdir(self, path):
        """
        Return True if path is a directory

        Implements the :func:`os.path.isdir` interface.

        """
        return util.is_dir(self._direntry(path))

    def isfile(self, path):
        """
        Return True if path is a file

        Implements the :func:`os.path.isfile` interface.

        """
        return util.is_file(self._direntry(path))

    def islink(self, path):
        """
        Return True if path is a symlink

        .. note::

            Currently hard-wired to return False

        """
        return False

    def makedirs(self, path):
        """Create directory entries for a path"""
        path = util.sanitize(path)
        new_entries = util.build_nested_dir_dict(path)
        util.merge_dicts(new_entries, self._entries)

    def listdir(self, path):
        """
        Return the directory contents of 'path'

        Implements the :func:`os.listdir` interface.
        :param path: filesystem path

        """
        direntry = self._direntry(path)
        if direntry is None:
            raise _OSError(errno.ENOENT, path)
        if util.is_file(direntry):
            raise _OSError(errno.ENOTDIR, path)
        if util.is_dir(direntry):
            entries = list(direntry.keys())
            entries.sort()
            return entries
        raise _OSError(errno.EINVAL, path)

    def walk(self, path):
        """
        Walk a filesystem path

        Implements the :func:`os.walk` interface.

        """
        path = util.sanitize(path)
        inspect = [path]
        while True:
            dirstack = []
            for entry in inspect:
                dirent = self._direntry(entry)
                dirs = []
                files = []
                if dirent:
                    for e in dirent:
                        if type(dirent[e]) is dict:
                            dirs.append(e)
                        else:
                            files.append(e)
                yield (entry, dirs, files)
                dirstack.extend([os.path.join(entry, d) for d in dirs])
            inspect = dirstack
            if not inspect:
                raise StopIteration

    def remove(self, path):
        """Remove the entry for a file path

        Implements the :func:`os.remove` interface.

        """
        path = util.sanitize(path)
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        entry = self._direntry(dirname)
        if type(entry) is not dict:
            raise _OSError(errno.ENOENT, path)

        try:
            del entry[basename]
        except KeyError:
            raise _OSError(errno.ENOENT, path)

    def rmdir(self, path):
        """Remove the entry for a directory path

        Implements the :func:`os.rmdir` interface.

        """
        path = util.sanitize(path)
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        entry = self._direntry(dirname)
        if not util.is_dir(entry):
            raise _OSError(errno.ENOENT, path)

        try:
            direntry = entry[basename]
        except KeyError:
            raise _OSError(errno.ENOENT, path)

        if len(direntry) != 0:
            raise _OSError(errno.ENOTEMPTY, path)

        del entry[basename]

    def copytree(self, src, dst):
        """Copy a directory subtree

        Implements the :func:`shutil.copytree` interface.

        """
        src_d = self._direntry(src)
        if src_d is None:
            raise _OSError(errno.ENOENT, src)
        dst = util.sanitize(dst)
        dst_d_parent = self._direntry(os.path.dirname(dst))
        dst_d_parent[os.path.basename(dst)] = copy.deepcopy(src_d)

    ## Internal Methods

    def _direntry(self, path):
        """Return the directory "dict" entry for a path"""
        path = util.sanitize(path)
        if path == '/':
            return self._entries
        elts = path.split('/')[1:]
        current = self._entries
        retval = None
        for elt in elts:
            if elt in current:
                retval = current[elt]
                current = current[elt]
            else:
                return None
        return retval
