import os
import glob

from mockfs.mfs import MockFS
from mockfs.mfs import builtins

__version__ = '0.8.0'


def install(entries=None):
    """
    Replace builtin functions with mockfs.

    :param entries: Dictionary mapping paths to content
    :rtype MockFS: Newly installed :class:`mockfs.MockFS` handler

    Example::

        import os
        import mockfs

        fs = mockfs.install()
        fs.add_entries({
                '/bin/sh': 'contents',
                '/bin/ls': 'contents',
        ])
        assert(os.listdir('/bin') == ['ls', 'sh'])

        mockfs.uninstall()

    """
    mfs = MockFS()
    if entries is not None:
        mfs.add_entries(entries)

    # Install functions
    os.chdir = mfs.cwd.chdir
    os.getcwd = mfs.cwd.getcwd
    os.getcwdu = mfs.cwd.getcwdu
    os.path.abspath = mfs.abspath
    os.path.exists = mfs.exists
    os.path.getsize = mfs.getsize
    os.path.islink = mfs.islink
    os.path.isdir = mfs.isdir
    os.path.isfile = mfs.isfile
    os.walk = mfs.walk
    os.listdir = mfs.listdir
    os.makedirs = mfs.makedirs
    os.remove = mfs.remove
    os.rmdir = mfs.rmdir
    glob.glob = mfs.glob

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
