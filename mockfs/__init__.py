import os
import glob
import shutil

from .mfs import MockFS
from .mfs import builtins
from .mfs import replace_builtins
from .mfs import restore_builtins
from . import compat
from . import storage

__version__ = '2.0.0'
