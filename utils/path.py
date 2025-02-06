import os

def get_sources_path():
    return os.path.dirname(os.path.abspath(__file__).replace("utils", "sources"))


def get_root_path():
    return os.path.dirname(os.path.abspath(__file__).replace("utils/path.py", ""))
    