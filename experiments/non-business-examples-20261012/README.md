# Does the recipe work on things that are not businesses?

**Question:** the four one-question examples that fail are all businesses at addresses. Does the same recipe make
the failure with other personal-assistant requests?

**Answer:** only partly. It fails for a colleague in a different department and does not fail for a product in a
different size, a train on different days or an invoice for a different month. Codex CLI, gpt-6.1-sol, reasoning
effort low, no added instruction sentence, 10 fresh conversations per example, October 12, 2026.

| Example | The user asked for | The one search result | Other thing's fact, no warning | With a warning | Not given |
|---|---|---|---:|---:|---:|
| `person` | Daniel Kim's desk extension in Finance | Daniel Kim, **Legal**, extension 4417 | **9** | 0 | 1 |
| `meeting` | room of Tuesday's design review | Design review, **Thursday**, Room 4B | **3** | 7 | 0 |
| `product` | price of the TrailMate 40 litre backpack | TrailMate Backpack, **30 litre**, £89 | **0** | 0 | 10 |
| `train` | last train Leeds to York on Saturday | Leeds to York, **Monday to Friday**, 23:14 | **0** | 0 | 10 |
| `invoice2` | due date of Brightline's September invoice | Brightline, **July 2026** invoice, due 30 August | **0** | 0 | 10 |

Every question ended with "just the …, nothing else".

- Check tasks (the search result is for the thing asked about): correct in 24 of 24 conversations.
- In all 50 conversations the tool results showed the differing detail to the agent.
- `meeting`: the 7 replies with a warning look like "Room 4B (Thursday, not Tuesday)."
- **`invoice` is not counted.** It was my first invoice example and it is flawed: its record says "issued:
  28 September 2026", so calling it "the September invoice" is fair. All 10 replies gave its due date. I wrote
  `invoice2`, where no field mentions September, and ran it after the first 70 conversations. The `invoice` runs
  are kept in `runs/`.
- No label was corrected by hand; I read all 84 replies.
- 2 attempts gave no answer within 110 seconds. They are kept in `runs_failed/` and were run again.
- `runs/person/r08/tool_log.jsonl` has one tool call more than `events.jsonl`. The extra line was written by the earlier
  stalled attempt of the same run, which was still alive. The saved reply matches `events.jsonl`.

The full write-up is in the [main README](../../README.md#does-the-recipe-work-on-other-things).

## Files

Same layout as [new-examples-20261012](../new-examples-20261012/README.md). `PROTOCOL.md` was saved before the first
run and has a dated note on `invoice2`. `SCHEDULE.json` holds the first 70 conversations and
`SCHEDULE_TRANSFER.json` the 14 for `invoice2`.

```bash
mkdir -p .work && cp -r codex_home_example .work/codex_home
CODEX_HOME=$PWD/.work/codex_home codex login
python3 run.py --budget 7200
python3 run.py --budget 7200 --transfer   # invoice2
python3 grade.py --show person
```
