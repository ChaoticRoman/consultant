import os

abspath = os.path.abspath(__file__)
script_dir = os.path.dirname(abspath)

def full_path(fn):
    return os.path.join(script_dir, fn)
