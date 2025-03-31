import os
from datetime import datetime as dt
from datetime import UTC

ISO8601 = "%Y-%m-%dT%H:%M:%SZ"

abspath = os.path.abspath(__file__)
script_dir = os.path.dirname(abspath)


def full_path(fn):
    return os.path.join(script_dir, fn)


def now2str():
    return dt.now(UTC).strftime(ISO8601)
