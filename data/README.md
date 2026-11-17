# Data

Raw files are **not committed** — they are gitignored. Download them yourself.

## Download

```bash
bash data/download.sh
```

Or by hand, into `data/raw/`:

| File | What it is |
|---|---|
| `email-Eu-core.txt.gz` | the edge list, `sender recipient` per line |
| `email-Eu-core-department-labels.txt.gz` | `node department`, 42 departments (0–41) |
| `email-Eu-core-temporal.txt.gz` | optional: `sender recipient time`, 332,334 timestamped emails |

All from https://snap.stanford.edu/data/

## Then build the graph

```bash
python3 src/build_graph.py
```

## On Windows

`bash data/download.sh` fails on Windows with errors like

    data/download.sh: line 4: cd: $'data\r': No such file or directory

because Git checks the script out with Windows line endings. Use the Python
downloader instead, which works everywhere:

    python src\download_data.py

(If you still want the bash route, `git pull` after the .gitattributes fix is
merged, then `rm data/download.sh && git checkout data/download.sh` to get a
clean copy.)

Writes `data/email-eu-core.gml` (directed, each node carries a `department`
attribute) and `data/summary.txt`.

## What to expect

SNAP publishes three different edge counts for this dataset. They all agree —
they count different things, and self-loops are the difference:

| Published | What it counts | Ours |
|---|---|---|
| 25,571 | every unique pair in the file, self-loops included | 25,571 |
| 25,552 | largest weakly connected component (986 nodes), self-loops included | 25,552 |
| 24,929 | that same component with self-loops removed | 24,929 |

The file contains 642 self-loops and no duplicate pairs. 623 of them sit inside
the large component (25,552 - 24,929); the other 19 belong to people whose only
record in the dataset is an email to themselves. Those 19 are exactly the nodes
that end up isolated once self-loops are dropped, which is why we keep them as
nodes: they are members of the organisation, and an attacker could still target
them.

Our own figures come from `summary.txt`, generated from the files. Our largest
SCC (803) and WCC (986) match SNAP's published values exactly, which is the check
that the pipeline reproduces the reference network.

## Caveats to state in the report

- An edge means *at least one* email was sent. It carries no volume or frequency.
- Only internal mail. Nothing entering or leaving the institution is recorded.
- There is no phishing in this data. We simulate the spread on a real contact
  network; the network is real, the outbreak is not.
