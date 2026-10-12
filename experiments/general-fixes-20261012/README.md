# Four short, general sentences on the six failing examples

**Question:** does a very short, general sentence in the agent's instructions stop the mistake? The mistake: the
user asks about one thing, the tool results hold the fact only for a similar thing, and the agent gives that fact
with no warning.

**Answer:** three of the four sentences do not stop it. "Ask the user when something is unclear." stops it on some
examples and not on others. Codex CLI, gpt-6.1-sol, reasoning effort low, 10 fresh conversations per version,
October 12, 2026.

Each sentence is added to the end of the first paragraph of the agent's instructions. Nothing else changes.

Number of the 10 conversations in which the reply gives the other thing's fact with no warning:

| Sentence added | Company | Pharmacy | Dental | Climbing | Books | Person | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| none | 8 | 6 | 10 | 10 | 5 | 10 | **49 of 60** |
| "State facts correctly." | 9 | 2 | 9 | 9 | 2 | 10 | **41 of 60** |
| "Do not make things up." | 9 | 4 | 9 | 10 | 5 | 10 | **47 of 60** |
| "You are allowed to say that you do not know." | 10 | 1 | 9 | 10 | 3 | 8 | **41 of 60** |
| "Ask the user when something is unclear." | 0 | 0 | 3 | 10 | 1 | 5 | **19 of 60** |

What the other replies did:

| Sentence added | Fact given with a warning | Fact not given | Typical reply that is not a mistake |
|---|---:|---:|---|
| none | 7 | 4 | "9:00 PM (Mission Street location)." |
| "State facts correctly." | 12 | 7 | "11:00 a.m. (Bay Street location)." |
| "Do not make things up." | 4 | 9 | "I couldn't verify a Grant Avenue number." |
| "You are allowed to say that you do not know." | 5 | 14 | "I don't know." |
| "Ask the user when something is unclear." | 1 | 40 | "Did you mean Northside Dental on Lake Street?" |

- **41 of 60 against 49 of 60** is a gap that appears by chance about 14 times in 100 (Fisher's exact test), so I
  cannot say that "State facts correctly." or "You are allowed to say that you do not know." helps. 47 of 60 is
  no change.
- **19 of 60 against 49 of 60** appears by chance less than 1 time in 1,000. "Ask the user…" helps. It gives 0 of
  10 on the company example, where the longer Sentences A and B gave 7 and 6 of 10. It gives 10 of 10 on the
  climbing example ("$28."), so it is not a fix.
- **Check tasks** (the tool result is for the thing asked about): correct in 96 of 96 conversations, 4 per sentence
  and example. None added doubt and none asked a question.
- 14 company replies have no "Product:" line. I labelled them by hand; each has its reason in
  `labels_override.json`. I read all 396 replies.
- 25 attempts gave no answer within 110 seconds. They are kept in `runs_failed/` and were run again. All 396
  planned conversations finished, and in all 396 the saved reply and the tool log match the recorded events.

The longer Sentences A, B and C on the same six examples, and the full write-up, are in the
[main README](../../README.md).

## Files

| File | What it is |
|---|---|
| `PROTOCOL.md` | The plan, saved before the first run |
| `conditions.py` | The four sentences and the list of versions |
| `first_study.py`, `new_examples.py` | The six examples, copied unchanged from the two earlier studies |
| `records_server.py` | The simulated tools the agent calls |
| `run.py`, `SCHEDULE.json` | Runs the conversations in Codex CLI; the shuffled order |
| `grade.py`, `labels.csv`, `labels_override.json` | The label of every last reply, with the reply text |
| `runs/<example>_<sentence>/rNN/` | One folder per conversation: instructions, records, messages, every tool call and result, every reply. `base` = no sentence, `_own` = check task |
| `runs_failed/` | The 25 attempts that stalled |

```bash
mkdir -p .work && cp -r codex_home_example .work/codex_home
CODEX_HOME=$PWD/.work/codex_home codex login
python3 run.py --budget 7200
python3 grade.py --show dental_ask
```
