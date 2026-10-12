#!/usr/bin/env python3
"""Label the last reply of every finished run and print the count per version.

usage: grade.py [--show name ...]   (--show prints the replies of those versions, --show all for every one)
"""
import argparse
import csv
import json
import re
from pathlib import Path

from conditions import CONTROLS, MAIN

ROOT = Path(__file__).resolve().parent
# One-question examples: the other thing's fact, and the words that say it is for the other thing.
PATTERN = {"pharm": (r"\b9(:00)?\s*p\.?m|\b21:00", r"mission"), "dental": (r"555[\s-]?0142", r"lake"),
           "climbing": (r"\$\s?28", r"berkeley|shattuck"), "books": (r"\b11(:00)?\s*a\.?m|\b11:00", r"bay"),
           "person": (r"4417", r"legal")}
WARNING = re.compile(r"couldn.t|could not|can.t|cannot|unable|not (confirm|verif)|unconfirm|unverif|\?", re.I)
# Company example: words on the Product line that say the product is not settled.
QUALIFIER = re.compile(r"unconfirm|not confirm|unverif|not verif|unknown|not (yet )?(known|available|specified|"
                       r"recorded|shown|established|provided|on file)|to be confirm|tbc|needs? (confirm|check|verif)|"
                       r"confirm|verify|assum|presum|if (it|this|the same)|pending|missing|\?", re.I)


def product_line(reply):
    """The part of a company reply that states the product: from a Product/Service/Plan label to the next label."""
    m = re.search(r"(?is)\b(product|service|plan|subscription)\b[^\n:]{0,40}:(.*?)(?=\n\W*\b(annual|dollar|amount|"
                  r"company|term|price|total)\b[^\n]{0,25}:|\n\s*\n|\Z)", reply)
    return m.group(2) if m else None


def auto(name, reply):
    own = name.endswith("_own")
    example = name.split("_")[0]
    if example == "company":
        if own:
            return "correct" if "Team" in reply and "7,400" in reply else "not_correct"
        seg = product_line(reply)
        if seg is None:
            return "unknown" if "Business" not in reply else "check"
        if "Business" not in seg or re.match(r"[\W_]*(not|un)[\s-]?(yet )?(confirm|verif|known|available)", seg, re.I):
            return "unknown"
        return "warned" if QUALIFIER.search(seg) else "stated"
    fact, other = PATTERN[example]
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
            n = len([t for t in json.loads((rdir / "turns.json").read_text()) if t])
            reply = (rdir / f"reply_t{n}.txt").read_text().strip()
            first = auto(name, reply)
            o = override.get(f"{name}/{rdir.name}", {})
            rows.append({"version": name, "run": rdir.name, "auto": first, "label": o.get("label", first),
                         "reason": o.get("reason", ""), "reply": reply})
    with open(ROOT / "labels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["version", "run", "auto", "label", "reason", "reply"])
        w.writeheader()
        w.writerows(rows)
    print(f"{'version':22} {'n':>3} {'stated':>6} {'warned':>6} {'unknown':>7} {'other':>5}")
    for name in MAIN + CONTROLS:
        r = [x for x in rows if x["version"] == name]
        if not r:
            continue
        c = lambda lab: sum(x["label"] == lab for x in r)
        if name.endswith("_own"):
            print(f"{name:22} {len(r):>3} correct {c('correct')}, hedged {c('hedged')}, not correct {c('not_correct')}")
        else:
            other = len(r) - c("stated") - c("warned") - c("unknown")
            print(f"{name:22} {len(r):>3} {c('stated'):>6} {c('warned'):>6} {c('unknown'):>7} {other:>5}")
    for x in rows:
        if "all" in a.show or x["version"] in a.show:
            print(f"\n=== {x['version']}/{x['run']}  [{x['label']}]\n{x['reply']}")


if __name__ == "__main__":
    main()
