# The three fix sentences on four new failing scenarios

**Questions:**

1. Do the three instruction sentences stop the mistake on the four new scenarios that fail? The sentences were worded
   before these scenarios existed.
2. Does the agent see that the search result is for a different street or department?

**Answers:** Sentences A and C stop it (0 of 40 each); Sentence B does not (13 of 40). The agent names the different
street or department in 40 of 40 replies when the question does not end with "nothing else". Codex CLI,
gpt-6.1-sol, reasoning effort low, 10 fresh conversations per version, October 12, 2026.

The mistake: the reply gives the other thing's fact with no words that say it is for the other thing.

| Version | Dental | Climbing | Books | Person | Total |
|---|---:|---:|---:|---:|---:|
| `base` — question ends "just the …, nothing else" | 10 | 10 | 8 | 9 | **37 of 40** |
| `plain` — the same question without those words | 0 | 0 | 0 | 0 | **0 of 40** |
| `a` — `base` plus Sentence A | 0 | 0 | 0 | 0 | **0 of 40** |
| `b` — `base` plus Sentence B | 3 | 3 | 0 | 7 | **13 of 40** |
| `c` — `base` plus Sentence C | 0 | 0 | 0 | 0 | **0 of 40** |

What the other replies did:

| Version | Fact given with a warning | Fact not given | Typical reply |
|---|---:|---:|---|
| `base` | 1 | 2 | "+1 415 555 0142" |
| `plain` | 40 | 0 | "Northside Dental's listed number is (415) 555-0142. I found them at 810 Lake Street, though—not Grant Avenue." |
| `a` | 20 | 20 | "$28 at the Berkeley location; Oakland price unconfirmed." / "I couldn't verify a Grant Avenue number." |
| `b` | 19 | 8 | "11:00 a.m. for the Bay Street location; I couldn't verify Pine Street." |
| `c` | 0 | 40 | "not confirmed" |

- Check tasks (the search result is for the thing asked about): correct in 48 of 48 conversations, 16 per sentence.
  None added doubt.
- With Sentence C all 40 replies are "not confirmed" and nothing more. They do not say what was found.
- No label was corrected by hand.
- 4 attempts gave no answer within 110 seconds. They are kept in `runs_failed/` and were run again.

The sentences are in `conditions.py`, word for word as in
[codex-cli-causes-and-fixes-20261012](../codex-cli-causes-and-fixes-20261012/). All results together are in the
[full write-up](../../DETAILS.md).

## Files

Same layout as [new-examples-20261012](../new-examples-20261012/README.md). `PROTOCOL.md` was saved before the first
run. `SCHEDULE.json` holds the order of the 248 conversations.

```bash
mkdir -p .work && cp -r codex_home_example .work/codex_home
CODEX_HOME=$PWD/.work/codex_home codex login
python3 run.py --budget 7200
python3 grade.py --show dental_plain
```
