#!/usr/bin/env bash
# Fetch the raw SNAP files into data/raw/
set -e
cd "$(dirname "$0")"
mkdir -p raw
cd raw

BASE=https://snap.stanford.edu/data

for f in email-Eu-core.txt.gz email-Eu-core-department-labels.txt.gz; do
  echo "downloading $f"
  curl -fL -O "$BASE/$f"
  gunzip -f "$f"
done

# optional: the time-ordered version, for a cascade that unfolds over 803 days
# curl -fL -O "$BASE/email-Eu-core-temporal.txt.gz" && gunzip -f email-Eu-core-temporal.txt.gz

echo
echo "done. now run:  python3 src/build_graph.py"
