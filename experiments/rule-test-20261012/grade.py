#!/usr/bin/env python3
"""Label the reply of every finished run and print the count per example.

usage: grade.py [--show name ...]   (--show prints the replies of those examples, --show all for every one)
"""
import argparse
import csv
import json
import re
from pathlib import Path

from conditions import EXAMPLES

ROOT = Path(__file__).resolve().parent
ORDER = ["product_colours", "train_minutes", "dental_offices", "person_two", "film", "restaurant", "parking",
         "library",
         "doctor", "museum", "band", "ticket", "report", "teacher", "product_onesize",
         "restaurant_far", "band_far", "film_far", "doctor_near", "museum_near", "dental_far"]
NO_CHECK = ("dental_offices", "person_two", "product_onesize", "restaurant_far", "band_far", "film_far",
            "doctor_near", "museum_near", "dental_far")
# The other thing's fact, and the words that say it is for the other thing.
PATTERN = {"product_colours": (r"slate|moss", r"30"), "train_minutes": (r"\b24\b", r"monday|week"),
           "dental_offices": (r"555[\s\-]?0142", r"lake"), "person_two": (r"4417", r"legal"),
           "film": (r"marsh", r"2021"), "restaurant": (r"22:30|10:30", r"vietnam"),
           "parking": (r"£\s?18", r"terminal 1|\bT1\b"), "library": (r"22:00|\b10(:00)?\s?p", r"south"),
           "doctor": (r"555[\s\-]?0164", r"dermat"), "museum": (r"£\s?14", r"\bart\b"), "band": (r"2009", r"norw"),
           "ticket": (r"£\s?24", r"adult"), "report": (r"4\.2", r"2024"), "teacher": (r"varga", r"year 8|\by8\b"),
           "product_onesize": (r"£\s?89", r"30"),
           "restaurant_far": (r"22:30|10:30", r"italian"), "band_far": (r"2009", r"japan"),
           "film_far": (r"marsh", r"1987"), "doctor_near": (r"555[\s\-]?0164", r"surg"),
           "museum_near": (r"£\s?14", r"natural"), "dental_far": (r"555[\s\-]?0142", r"chicago|lake")}
EXCLUDED = {}
WARNING = re.compile(r"couldn.t|could not|can.t|cannot|unable|not (confirm|verif)|unconfirm|unverif|\?", re.I)


def auto(name, reply):
    own = name.endswith("_own")
    fact, other = PATTERN[name[:-4] if own else name]
    if own:
        return "correct" if re.search(fact, reply, re.I) else "not_correct"
    if name in EXCLUDED:
        return "excluded"
    if not re.search(fact, reply, re.I):
        return "unknown"
    return "warned" if re.search(other, reply, re.I) or WARNING.search(reply) else "stated"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", nargs="*", default=[])
    a = ap.parse_args()
    over_path = ROOT / "labels_override.json"
    override = json.loads(over_path.read_text()) if over_path.exists() else {}
    names = ORDER + [v + "_own" for v in ORDER if v not in NO_CHECK]
    assert set(ORDER) == set(EXAMPLES)
    rows = []
    for name in names:
        for rdir in sorted((ROOT / "runs" / name).glob("r*")):
            if not (rdir / "meta.json").exists():
                continue
            reply = (rdir / "reply_t1.txt").read_text().strip()
            first = auto(name, reply)
            o = override.get(f"{name}/{rdir.name}", {})
            rows.append({"example": name, "run": rdir.name, "auto": first, "label": o.get("label", first),
                         "reason": o.get("reason", EXCLUDED.get(name, "")), "reply": reply})
    with open(ROOT / "labels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["example", "run", "auto", "label", "reason", "reply"])
        w.writeheader()
        w.writerows(rows)
    print(f"{'example':14} {'n':>3} {'stated':>6} {'warned':>6} {'unknown':>7}")
    for name in names:
        r = [x for x in rows if x["example"] == name]
        if not r:
            continue
        c = lambda lab: sum(x["label"] == lab for x in r)
        if name.endswith("_own"):
            print(f"{name:14} {len(r):>3} correct {c('correct')} of {len(r)}")
        elif name in EXCLUDED:
            print(f"{name:14} {len(r):>3} not counted: {EXCLUDED[name]}")
        else:
            print(f"{name:14} {len(r):>3} {c('stated'):>6} {c('warned'):>6} {c('unknown'):>7}")
    for x in rows:
        if "all" in a.show or x["example"] in a.show:
            print(f"\n=== {x['example']}/{x['run']}  [{x['label']}]\n{x['reply']}")


if __name__ == "__main__":
    main()
