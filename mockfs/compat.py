from __future__ import absolute_import, division, unicode_literals
import sys


PY2 = sys.version_info[0] == 2
if PY2:
    import __builtin__ as builtins

    int_types = (int, long)  # noqa
    string_types = (str, unicode)  # noqa
else:
    import builtins  # noqa

    int_types = (int,)
    string_types = (str,)
