import os

from mockfs.mfs import MockFS

__version__ = '0.6.0'

# Python functions to replace
builtins = {
    'os.path.exists': os.path.exists,
    'os.path.islink': os.path.islink,
    'os.path.isdir': os.path.isdir,
    'os.path.isfile': os.path.isfile,
    'os.walk': os.walk,
    'os.listdir': os.listdir,
}


def install(entries=None, pathmap=None):
    """
    Replace builtin modules with mockfs equivalents.

    :param entries: Dictionary mapping paths to content
    :rtype MockFS: Newly installed :class:`mockfs.mfs.MockFS` handler

    Example::

        import mockfs

        mfs = mockfs.install(entries={'/bin/ls': 'content'})

    """
    mfs = MockFS(entries=entries, pathmap=pathmap)
    os.path.exists = mfs.exists
    os.path.islink = mfs.islink
    os.path.isdir = mfs.isdir
    os.path.isfile = mfs.isfile
    os.walk = mfs.walk
    os.listdir = mfs.listdir

    return mfs


def uninstall():
    """Restore the original builtin functions."""
    for k, v in builtins.items():
        mod, func = k.rsplit('.', 1) # 'os.path.isdir' -> ('os.path', 'isdir')
        name_elts = mod.split('.')
        top = name_elts.pop(0)
        module = globals()[top]
        for elt in name_elts:
            module = getattr(module, elt)
        setattr(module, func, v)
