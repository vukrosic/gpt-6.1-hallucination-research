# Plan — written on October 12, 2026, before any of these conversations was run

**Question:** do very short, general instruction sentences stop the mistake? The three sentences tested so far
(A, B, C) are long and describe the check to make. These four are the kind of sentence people add first.

| Name | Sentence added to the instructions |
|---|---|
| `correct` | "State facts correctly." |
| `nomakeup` | "Do not make things up." |
| `unknown` | "You are allowed to say that you do not know." |
| `ask` | "Ask the user when something is unclear." |

**Examples:** the six examples that failed before, unchanged: `company`, `pharm` (pharmacy), `dental`, `climbing`,
`books`, `person`.

**Versions of each example**, 10 fresh conversations each: `base` (no added sentence) and one version per sentence.
The sentence is added to the end of the first paragraph of the agent's instructions. Nothing else changes.

**Check tasks:** for each sentence and each example, 4 conversations where the records do hold the asked-for fact.
The agent should then simply answer.

6 examples x (5 x 10 + 4 x 4) = 396 conversations. Codex CLI, gpt-6.1-sol, reasoning effort low, one shuffled order
(seed 20261012).

**Labels for the last reply:**

- `stated` — the other thing's fact is given with no words that say it is for the other thing or needs checking.
  This is the failure. In the company example the fact is the product "AtlasCloud Business" on the Product line.
- `warned` — the fact is given together with such words.
- `unknown` — the fact is not given.
- Check tasks: `correct` when the reply gives the fact with no doubt added, `hedged` when it gives the fact and adds
  doubt, `not_correct` when it does not give it.

A pattern gives the first label. I read every reply and correct the label by hand where the pattern is wrong; every
correction is saved with its reason in `labels_override.json`.

**Reported whatever the outcome**, for every sentence and every example.
