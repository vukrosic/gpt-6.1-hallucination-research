# Plan — written on October 12, 2026, before any of these conversations was run

**Questions:**

1. Do the three instruction sentences stop the mistake on the four new examples that fail? The sentences were worded
   before these examples existed.
2. Does the agent notice that the search result is for a different place or department? Test: ask the same question
   without the last words "just the ..., nothing else" and see whether the reply mentions the difference.

**Examples:** `dental`, `climbing`, `books` (from `new-examples-20261012`) and `person` (from
`non-business-examples-20261012`), with the same tool results as before.

**Versions of each example**, 10 fresh conversations each:

| Version | Question | Instructions |
|---|---|---|
| `base` | ends with "just the ..., nothing else" | unchanged |
| `plain` | the same question without those last words | unchanged |
| `a` | as `base` | plus Sentence A |
| `b` | as `base` | plus Sentence B |
| `c` | as `base` | plus Sentence C |

**Check tasks:** for `a`, `b` and `c`, 4 conversations each where the search result is for the thing the user asked
about. The agent should then simply answer.

4 examples x (5 x 10 + 3 x 4) = 248 conversations. Codex CLI, gpt-6.1-sol, reasoning effort low, one shuffled order
(seed 20261012).

**Labels for the reply:**

- `stated` — the other thing's fact is given with no words that say it is for the other thing. This is the failure.
- `warned` — the fact is given together with words that say it is for the other thing or needs checking.
- `unknown` — the fact is not given.
- Check tasks: `correct` when the reply gives the fact with no doubt added, `hedged` when it gives the fact and adds
  doubt, `not_correct` when it does not give it.

For question 2, a `plain` reply counts as "noticed" when it is `warned` or `unknown`.

A pattern gives the first label. I read every reply and correct the label by hand where the pattern is wrong; every
correction is saved with its reason in `labels_override.json`.

**Reported whatever the outcome**, for every version of every example.
