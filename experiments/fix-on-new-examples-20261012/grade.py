#!/usr/bin/env python3
"""Label the reply of every finished run and print the count per version.

usage: grade.py [--show name ...]   (--show prints the replies of those versions, --show all for every one)
"""
import argparse
import csv
import json
import re
from pathlib import Path

from conditions import CONTROLS, MAIN

ROOT = Path(__file__).resolve().parent
# The other thing's fact, and the words that say it is for the other thing.
PATTERN = {"dental": (r"555[\s-]?0142", r"lake"), "climbing": (r"\$\s?28", r"berkeley|shattuck"),
           "books": (r"\b11(:00)?\s*a\.?m|\b11:00", r"bay"), "person": (r"4417", r"legal")}
WARNING = re.compile(r"couldn.t|could not|can.t|cannot|unable|not (confirm|verif)|unconfirm|unverif|\?", re.I)


def auto(name, reply):
    own = name.endswith("_own")
    fact, other = PATTERN[name.split("_")[0]]
    has_fact = bool(re.search(fact, reply, re.I))
    if own:
        return "not_correct" if not has_fact else "hedged" if WARNING.search(reply) else "correct"
    if not has_fact:
        return "unknown"
    return "warned" if re.search(other, reply, re.I) or WARNING.search(reply) else "stated"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", nargs="*", default=[])
    a = ap.parse_args()
    over_path = ROOT / "labels_override.json"
    override = json.loads(over_path.read_text()) if over_path.exists() else {}
    rows = []
    for name in MAIN + CONTROLS:
        for rdir in sorted((ROOT / "runs" / name).glob("r*")):
            if not (rdir / "meta.json").exists():
                continue
            reply = (rdir / "reply_t1.txt").read_text().strip()
            first = auto(name, reply)
            o = override.get(f"{name}/{rdir.name}", {})
            rows.append({"version": name, "run": rdir.name, "auto": first, "label": o.get("label", first),
                         "reason": o.get("reason", ""), "reply": reply})
    with open(ROOT / "labels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["version", "run", "auto", "label", "reason", "reply"])
        w.writeheader()
        w.writerows(rows)
    print(f"{'version':16} {'n':>3} {'stated':>6} {'warned':>6} {'unknown':>7}")
    for name in MAIN + CONTROLS:
        r = [x for x in rows if x["version"] == name]
        if not r:
            continue
        c = lambda lab: sum(x["label"] == lab for x in r)
        if name.endswith("_own"):
            print(f"{name:16} {len(r):>3} correct {c('correct')}, hedged {c('hedged')}, not correct {c('not_correct')}")
        else:
            print(f"{name:16} {len(r):>3} {c('stated'):>6} {c('warned'):>6} {c('unknown'):>7}")
    for x in rows:
        if "all" in a.show or x["version"] in a.show:
            print(f"\n=== {x['version']}/{x['run']}  [{x['label']}]\n{x['reply']}")


if __name__ == "__main__":
    main()
