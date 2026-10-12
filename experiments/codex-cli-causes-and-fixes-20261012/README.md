# Causes and fixes in Codex CLI (October 12, 2026)

268 fresh gpt-6.1-sol conversations in Codex CLI: the company example with one thing changed at a time, three
instruction sentences on the company, school and pharmacy examples, and check tasks where the asked-for fact is in the
records.

**The results and their explanation are in the [main README](../../README.md).** This folder holds the code and every
conversation.

| File | What it is |
|---|---|
| `PROTOCOL.md` | The plan and the labels, written before the runs, with a dated note on what was added later |
| `conditions.py` | The records, the messages, the three sentences and every one-change version |
| `records_server.py` | The simulated tools the agent calls |
| `run.py` | Runs the conversations in Codex CLI in a shuffled order (`SCHEDULE*.json`) |
| `grade.py`, `labels.csv`, `labels_override.json` | The label of every last reply, with the reply text |
| `runs/<version>/rNN/` | One folder per conversation: `instructions.md`, `records.json`, `turns.json` (the user's messages), `events.jsonl` and `tool_log.jsonl` (every tool call and result), `reply_tN.txt` (the reply after message N), `meta.json` (timing and token counts) |
| `runs_failed/` | The 22 attempts that stalled or were stopped; each was run again |
| `smoke/` | One trial conversation from before the schedule was fixed; not counted |
| `codex_home_example/` | The Codex settings used: no shell, no web search, no saved notes, only the simulated tools |

Version names: `base` is the unchanged company example. `school_…` and `pharm_…` are the other two examples.
`inst_general`, `inst_source` and `inst_field` add Sentence A, B and C. A name ending in `_own` is a check task.

`python3 grade.py` prints the counts from the saved conversations; it needs no model access.
