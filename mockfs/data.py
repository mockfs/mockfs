_data = None

def instance():
    global _data
    if _data is None:
        _data = Data()
    return _data


def uninstall():
    global _data
    _data = None
