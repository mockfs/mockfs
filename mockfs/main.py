"""mockfs: A simple mock filesystem for unit tests."""

import os
import glob


# Static MockFS instance
_mockfs = None

def singleton(entries=None, pathmap=None):
    """Return a global MockFS singleton."""
    global _mockfs
    if not _mockfs:
        _mockfs = MockFS(entries=entries, pathmap=pathmap)
    return _mockfs


def uninstall():
    global _mockfs
    _mockfs = None


def _build_nested_dict(entries):
    """Convert a flat dict of paths to a nested dict."""
    if not entries:
        return {}

    result = {}
    for raw_path, value in entries.items():
        path = _sanitize(raw_path)
        basename = os.path.basename(path)
        subpaths = path.split('/')[1:]
        subentry = result
        current = subentry
        for subpath in subpaths:
            current = subentry
            subentry = subentry.setdefault(subpath, {})
        current[basename] = value

    return result


def _merge_dicts(src, dst):
    """
    Return a new dictionary with entries from A merged into B.

    :param src: source dictionary
    :param dst: destination dictionary

    """
    for k, v in src.items():
        if k not in dst:
            dst[k] = v
            continue

        if type(dst[k]) is dict:
            if type(v) is dict:
                dst[k] = _merge_dicts(dst[k], v)
            else:
                dst[k] = v
            continue


def _sanitize(path):
    """
    Clean up path arguments for use with MockFS

    MockFS isn't happy with trailing slashes since it uses a dict
    to simulate the file system.

    """
    while '//' in path:
        path = path.replace('//', '/')
    while len(path) > 1 and path.endswith('/'):
        path = path[:-1]
    return path



class MockFS(object):
    """
    Provides implementations for functions in ``os``, ``os.path``, and ``glob``."""

    def __init__(self, entries=None, pathmap=None):
        self._entries = _build_nested_dict(entries)
        self._pathmap = pathmap
        self._inwalk = False
        self._path = None
        self._walkdir = self._entries

    def add_entries(self, entries):
        """Add new entries to mockfs."""
        new_entries = _build_nested_dict(entries)
        _merge_dicts(new_entries, self._entries)

    def exists(self, path):
        path = _sanitize(path)
        dirent = self._direntry(os.path.dirname(path))
        if path == '/':
            return bool(dirent)
        return dirent and os.path.basename(path) in dirent

    def isdir(self, path):
        path = _sanitize(path)
        return type(self._direntry(path)) is dict

    def isfile(self, path):
        return not self.isdir(path)

    def listdir(self, path):
        path = _sanitize(path)
        direntry = self._direntry(path)
        if direntry:
            entries = list(direntry.keys())
            entries.sort()
            return entries
        return []

    def islink(self, path):
        path = _sanitize(path)
        return False

    def walk(self, path):
        path = _sanitize(path)
        entries = []
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

    def _direntry(self, path):
        path = _sanitize(path)
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
