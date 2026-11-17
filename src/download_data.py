"""Download the raw SNAP files. Works on Windows, macOS and Linux.

    python3 src/download_data.py        (or: python src\download_data.py)

Use this instead of data/download.sh if you are on Windows or do not have
bash. It needs nothing beyond the Python standard library.
"""

import gzip
import os
import shutil
import sys
import urllib.request

BASE = "https://snap.stanford.edu/data"
FILES = [
    "email-Eu-core.txt.gz",
    "email-Eu-core-department-labels.txt.gz",
]
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "data", "raw")


def fetch(name):
    out = os.path.join(RAW, name[:-3])          # strip .gz
    if os.path.isfile(out):
        print("already have %s" % os.path.basename(out))
        return
    url = "%s/%s" % (BASE, name)
    gz = os.path.join(RAW, name)
    print("downloading %s" % name)
    try:
        urllib.request.urlretrieve(url, gz)
    except Exception as exc:
        sys.exit(
            "could not download %s\n  %s\n\n"
            "If your network blocks snap.stanford.edu, open this in a browser:\n"
            "  %s\n"
            "and save the unzipped file as data/raw/%s"
            % (url, exc, url, os.path.basename(out))
        )
    with gzip.open(gz, "rb") as src, open(out, "wb") as dst:
        shutil.copyfileobj(src, dst)
    os.remove(gz)
    print("  -> data/raw/%s" % os.path.basename(out))


def main():
    os.makedirs(RAW, exist_ok=True)
    for name in FILES:
        fetch(name)
    print("\ndone. now run:  python3 src/build_graph.py")


if __name__ == "__main__":
    main()
