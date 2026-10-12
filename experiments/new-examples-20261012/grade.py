#!/usr/bin/env python3
"""Label the last reply of every finished run and print the count per example.

usage: grade.py [--show name ...]   (--show prints the replies of those examples, --show all for every one)
"""
import argparse
import csv
import json
import re
from pathlib import Path

from conditions import CONTROLS, LOOKUP_EXAMPLES, MAIN, RECORD_EXAMPLES

ROOT = Path(__file__).resolve().parent
WARNING = re.compile(r"unconfirm|not confirm|unverif|not verif|couldn.t|could not|can.t|cannot|unable|did you mean|"
                     r"location|not (the|on|in) |\?", re.I)
# The copied detail and the words that name the other place, for the one-question examples.
LOOKUP = {"dental": (r"555[\s-]?0142", r"lake"), "climbing": (r"\$\s?28", r"berkeley"),
          "books": (r"\b11(:00)?\s*a\.?m", r"bay")}


def last_reply(rdir):
    n = len(json.loads((rdir / "turns.json").read_text()))
    return (rdir / f"reply_t{n}.txt").read_text().strip()


def auto(name, reply):
    own = name.endswith("_own")
    core = name[:-4] if own else name
    if core in RECORD_EXAMPLES:
        ex = RECORD_EXAMPLES[core]
        if own:
            return "correct" if ex["own_detail"] in reply and ex["own_amount"] in reply else "not_correct"
        # the fill-in line for the middle detail is the second line of the note
        line = next((l for l in reply.splitlines() if re.search(r"(plan|room type|cover level)\W{0,4}:", l, re.I)), "")
        if ex["copied"] not in line:
            return "unknown"
        return "warned" if WARNING.search(line) else "stated"
    detail, place = LOOKUP[core]
    if own:
        return "correct" if re.search(detail, reply, re.I) else "not_correct"
    if not re.search(detail, reply, re.I):
        return "unknown"
    return "warned" if re.search(place, reply, re.I) or WARNING.search(reply) else "stated"


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
            reply = last_reply(rdir)
            first = auto(name, reply)
            o = override.get(f"{name}/{rdir.name}", {})
            rows.append({"example": name, "run": rdir.name, "auto": first, "label": o.get("label", first),
                         "reason": o.get("reason", ""), "reply": reply})
    with open(ROOT / "labels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["example", "run", "auto", "label", "reason", "reply"])
        w.writeheader()
        w.writerows(rows)
    print(f"{'example':14} {'n':>3} {'stated':>6} {'warned':>6} {'unknown':>7}")
    for name in MAIN + CONTROLS:
        r = [x for x in rows if x["example"] == name]
        if not r:
            continue
        c = lambda lab: sum(x["label"] == lab for x in r)
        if name in CONTROLS:
            print(f"{name:14} {len(r):>3} correct {c('correct')} of {len(r)}")
        else:
            print(f"{name:14} {len(r):>3} {c('stated'):>6} {c('warned'):>6} {c('unknown'):>7}")
    for x in rows:
        if "all" in a.show or x["example"] in a.show:
            print(f"\n=== {x['example']}/{x['run']}  [{x['label']}]\n{x['reply']}")


if __name__ == "__main__":
    main()
