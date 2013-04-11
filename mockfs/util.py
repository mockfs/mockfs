import os


def is_file(entry):
    return isinstance(entry, basestring)


def is_dir(entry):
    return type(entry) is dict


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
            dst[k] = merge_dicts(v, dst[k])
            continue
        if type(dst[k]) is list and type(v) is list:
            dst[k].extend(v)
            continue
        dst[k] = v
    return dst


def build_nested_dict(entries):
    """
    Convert a flat dict of paths to a nested dict

    :param entries: Path to entry dictionary
    :type entries: :py:data:`dict`

    e.g. `{'/unix/path': 'content', '/unix/dir': {},}`

    """
    result = {}
    if not entries:
        return {}
    # Each entry key is either a file path or an empty directory.
    # Directories are represented by dictionaries, the empty dictionary
    # can be passed as a value to indicate an empty directory.
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


def build_nested_dir_dict(dirpath):
    """Build a nested dict of dicts from a directory path

    :param dirpath: Directory path
    :type dirpath: :py:data:`str`

    """
    result = {}
    path = sanitize(dirpath)
    basename = os.path.basename(path)
    subpaths = path.split('/')[1:]

    subentry = result
    current = subentry
    for subpath in subpaths:
        current = subentry
        subentry = subentry.setdefault(subpath, {})

    current[basename] = {}
    return result
