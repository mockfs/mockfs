import os

from mockfs import main
from mockfs import data

__version__ = '0.5.0'

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

    Example::

        install({'/bin/ls': 'content'})

    """
    mockfs = main.singleton(entries=entries, pathmap=pathmap)
    os.path.exists = mockfs.exists
    os.path.islink = mockfs.islink
    os.path.isdir = mockfs.isdir
    os.path.isfile = mockfs.isfile
    os.walk = mockfs.walk
    os.listdir = mockfs.listdir


def uninstall():
    """Restore the original builtin functions."""
    # Remove the static MockFS instance
    for k, v in builtins.items():
        mod, func = k.rsplit('.', 1)
        item = None
        for elt in mod.split('.'):
            if item is None:
                item = globals()[elt]
            else:
                item = getattr(item, elt)
        setattr(item, func, v)

    # Teardown submodules
    main.uninstall()
    data.uninstall()

def add_entries(entries):
    """Add entries to the global mockfs singleton."""
    main.singleton().add_entries(entries)
