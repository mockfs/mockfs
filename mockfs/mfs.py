"""mockfs: A simple mock filesystem for unit tests."""

import os
import copy
import errno

from mockfs import util


def _raise_OSError(err, path):
    """Raise an OSError with an appropriate error string"""
    raise OSError(err, os.strerror(err) + ": '%s'" % path)


class MockFS(object):
    """
    MockFS implementation object

    Provides stubs for functions in :mod:`os`, :mod:`os.path`, and :mod:`glob`.

    """

    def __init__(self, entries=None, pathmap=None):
        self._entries = util.build_nested_dict(entries)
        self._pathmap = pathmap
        self._inwalk = False
        self._path = None
        self._walkdir = self._entries

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
        path = util.sanitize(path)
        return type(self._direntry(path)) is dict

    def isfile(self, path):
        """
        Return True if path is a file

        Implements the :func:`os.path.isfile` interface.

        """
        path = util.sanitize(path)
        return isinstance(self._direntry(path), basestring)

    def islink(self, path):
        """
        Return True if path is a symlink

        .. note::

            Currently hard-wired to return False

        """
        path = util.sanitize(path)
        return False

    def makedirs(self, path):
        """Create directory entries for a path"""
        path = util.sanitize(path)
        new_entries = util.build_nested_dir_dict([path])
        util.merge_dicts(new_entries, self._entries)


    def listdir(self, path):
        """
        Return the directory contents of 'path'

        Implements the :func:`os.listdir` interface.
        :param path: filesystem path

        """
        path = util.sanitize(path)
        direntry = self._direntry(path)
        if direntry is None:
            _raise_OSError(errno.ENOENT, path)
        else:
            entries = list(direntry.keys())
            entries.sort()
            return entries

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
                break
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
            _raise_OSError(errno.ENOENT, path)

        try:
            del entry[basename]
        except KeyError:
            _raise_OSError(errno.ENOENT, path)

    def rmdir(self, path):
        """Remove the entry for a directory path

        Implements the :func:`os.rmdir` interface.

        """
        path = util.sanitize(path)
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        entry = self._direntry(dirname)
        if type(entry) is not dict:
            _raise_OSError(errno.ENOENT, path)

        try:
            direntry = entry[basename]
        except KeyError:
            _raise_OSError(errno.ENOENT, path)

        if len(direntry) != 0:
            _raise_OSError(errno.ENOTEMPTY, path)

        del entry[basename]

    def copytree(self, src, dst):
        """Copy a directory subtree

        Implements the :func:`shutil.copytree` interface.

        """
        src = util.sanitize(src)
        dst = util.sanitize(dst)
        src_d = self._direntry(src)
        if src_d is None:
            _raise_OSError(errno.ENOENT, src)
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
