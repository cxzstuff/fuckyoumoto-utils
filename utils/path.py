import os

def get_sources_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sources"))

def get_root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
