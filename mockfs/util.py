import os
import copy


def sanitize(path):
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


def merge_dicts(src, dst):
    """
    Merge entries from 'src' into 'dst'.

    :param src: source dictionary
    :param dst: destination dictionary

    """
    for k, v in src.items():
        if k not in dst:
            dst[k] = v
            continue
        if type(dst[k]) is dict:
            dst[k] = merge_dicts(dst[k], v)
            continue
        if type(dst[k]) is list and type(v) is list:
            dst[k].extend(v)
            continue
        dst[k] = v
    return dst


def build_nested_dict(entries):
    """Convert a flat dict of paths to a nested dict."""
    result = {}
    if not entries:
        return {}
    for raw_path, value in entries.items():
        path = sanitize(raw_path)
        basename = os.path.basename(path)
        subpaths = path.split('/')[1:]
        subentry = result
        current = subentry
        for subpath in subpaths:
            current = subentry
            subentry = subentry.setdefault(subpath, {})
        current[basename] = value
    return result
