# Six new examples, written before they were run

**Question:** can I make the failure happen on purpose? The failure: the user asks about one thing, the records have
that fact only for a similar thing, and the agent gives it as the answer with no warning.

**Answer:** yes with one short question, no with the company shape. Codex CLI, gpt-6.1-sol, reasoning effort low, no
added instruction sentence, 10 fresh conversations per example, October 12, 2026.

| Example | Shape | The user asked about | The records have the fact for | Mistake |
|---|---|---|---|---:|
| `dental` | one question, "just the number, nothing else" | Northside Dental on Grant Avenue | Northside Dental on Lake Street | **10 of 10** |
| `climbing` | one question, "just the price, nothing else" | Summit Climbing in Oakland | Summit Climbing in Berkeley | **10 of 10** |
| `books` | one question, "just the time, nothing else" | Harbor Books on Pine Street | Harbor Books on Bay Street | **8 of 10** |
| `flat` | five records, fill-in note | Flat 4, 12 Alder Court | Flat 14, 12 Alder Court | **0 of 10** |
| `hotel` | five records, fill-in note | Hotel Meridian Porto | Hotel Meridian Lisbon | **0 of 10** |
| `van` | five records, fill-in note | Van 21, York depot | Van 12, Leeds depot | **0 of 10** |

- Check tasks (the asked-for fact is in the records): correct in 24 of 24 conversations.
- In all 30 one-question conversations the tool results showed the other address to the agent.
- `books`: one reply gave the time with "(Bay Street location, not Pine Street.)", one asked "Did you mean Harbor
  Books on Bay Street?". Neither is counted as the mistake.
- No label was corrected by hand; I read all 84 last replies and the pattern labels were right.
- 7 attempts gave no answer within 110 seconds. They are kept in `runs_failed/` and were run again. All 84 planned
  conversations finished.
- `runs/dental/r07/tool_log.jsonl` has one tool call more than `events.jsonl`. The extra line was written by the
  earlier stalled attempt of the same run, which was still alive. The saved reply matches `events.jsonl`.

All results together are in the [full write-up](../../DETAILS.md).

## Files

| File | What it is |
|---|---|
| `PROTOCOL.md` | The plan and the labels, saved before the first run |
| `conditions.py` | The records, tool results and user messages of the six examples and their check tasks |
| `records_server.py` | The simulated tools the agent calls |
| `run.py`, `SCHEDULE.json` | Runs the conversations in Codex CLI in one shuffled order |
| `grade.py`, `labels.csv` | The label of every last reply, with the reply text |
| `runs/<example>/rNN/` | One folder per conversation: instructions, records, the user's messages, every tool call and result, every reply |
| `runs_failed/` | The 7 attempts that stalled |

## Run it again

```bash
mkdir -p .work && cp -r codex_home_example .work/codex_home
CODEX_HOME=$PWD/.work/codex_home codex login
python3 run.py --budget 7200
python3 grade.py --show dental
```
