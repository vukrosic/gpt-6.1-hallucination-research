#!/usr/bin/env python3
"""Write EXAMPLES.md: every one-question example with its question, its one search result and all 10 saved replies.

Nothing is typed by hand: questions, search results, replies and labels are read from the experiment folders.
usage: python3 make_examples_page.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXP = ROOT / "experiments"
NEW, NONB, RULE, FIRST = ("new-examples-20261012", "non-business-examples-20261012", "rule-test-20261012",
                          "codex-cli-causes-and-fixes-20261012")
WORDS = {"stated": "WRONG ANSWER: gives the similar thing's fact and does not say whose it is",
         "warned": "gives the similar thing's fact and says whose it is",
         "unknown": "does not give the fact"}
SECTIONS = [
    ("1. Close detail: the agent gives a wrong answer",
     "The user's detail and the search result's detail are different and close.",
     [(NEW, "dental"), (NEW, "climbing"), (RULE, "restaurant"), (RULE, "band"), (RULE, "doctor_near"),
      (RULE, "museum_near"), (RULE, "film"), (NONB, "person"), (NEW, "books"), (FIRST, "pharm_base")]),
    ("2. The same examples with a far detail",
     "The question is the same as in section 1. One value in the search result is changed.",
     [(RULE, "doctor"), (RULE, "museum"), (RULE, "dental_far"), (RULE, "film_far"), (RULE, "band_far"),
      (RULE, "restaurant_far")]),
    ("3. The user's detail picks one of a set: no wrong answers",
     "Sizes, timetable days, invoice months, terminals, campuses, ticket types, report years, year groups.",
     [(NONB, "product"), (RULE, "product_colours"), (RULE, "product_onesize"), (NONB, "train"),
      (RULE, "train_minutes"), (NONB, "invoice2"), (RULE, "parking"), (RULE, "library"), (RULE, "ticket"),
      (RULE, "report"), (RULE, "teacher")]),
    ("4. One field says that several exist: no wrong answers",
     "The dentist and colleague examples of section 1 with one field added to the search result.",
     [(RULE, "dental_offices"), (RULE, "person_two")]),
    ("5. A different weekday: in between",
     "", [(NONB, "meeting")]),
]


def labels(folder):
    rows = list(csv.DictReader(open(EXP / folder / "labels.csv")))
    key = "example" if "example" in rows[0] else "version"
    return {(r[key], r["run"]): r["label"].replace("plan_", "") for r in rows}


def main():
    out = ["# Every one-question example, with all replies", "",
           "This page is made by `make_examples_page.py` from the saved conversations. Each example shows the user's "
           "one message, the one result the search tool returned, and the agent's reply in each of the 10 "
           "conversations. Agent: Codex CLI with gpt-6.1-sol, no sentence added to the instructions.", "",
           "The environment is simulated: the search tool and the records it returns are written for these tests, "
           "and web search is switched off. The **similar thing** is the one "
           "entry the search returns: it has the same name as the thing the user asked about and one different "
           "detail (another street, another department, another year).", "",
           "- **WRONG ANSWER** = the reply gives the similar thing's fact and does not say whose it is.",
           "- **fact with a warning** = the reply gives the similar thing's fact and says whose it is.",
           "- **fact not given** = the reply does not give the fact.", ""]
    summary = ["| Section | Example | Wrong answers | Fact with a warning | Fact not given |", "|---|---|---:|---:|---:|"]
    body = []
    for title, note, items in SECTIONS:
        body += [f"## {title}", ""] + ([note, ""] if note else [])
        for folder, name in items:
            lab = labels(folder)
            runs = sorted((EXP / folder / "runs" / name).glob("r*"))
            first = runs[0]
            turn = json.loads((first / "turns.json").read_text())[0]
            rec = json.loads((first / "records.json").read_text())
            result = next(v["results"][0] for k, v in rec.items() if isinstance(v, dict) and "results" in v)
            got = [lab[(name, r.name)] for r in runs]
            count = {k: got.count(k) for k in WORDS}
            anchor = f"{name}"
            summary.append(f"| {title.split('.')[0]} | [`{name}`](#{anchor}) | {count['stated']} of {len(runs)} | "
                           f"{count['warned']} | {count['unknown']} |")
            body += [f"### `{name}`", "",
                     f"**The user asks:** \"{turn}\"", "",
                     "**The only search result:**", "", "```json", json.dumps(result, ensure_ascii=False), "```", "",
                     f"**Result:** {count['stated']} wrong answers in {len(runs)} conversations, "
                     f"{count['warned']} fact with a warning, {count['unknown']} fact not given. "
                     f"Saved in `experiments/{folder}/runs/{name}/`.", "",
                     "| Run | Reply | What it is |", "|---|---|---|"]
            for r in runs:
                reply = (r / "reply_t1.txt").read_text().strip().replace("\n", " ").replace("|", "\\|")
                body.append(f"| {r.name} | {reply} | {WORDS[lab[(name, r.name)]].split(':')[0]} |")
            body.append("")
    (ROOT / "EXAMPLES.md").write_text("\n".join(out + summary + [""] + body))
    print(len(summary) - 2, "examples")


if __name__ == "__main__":
    main()
