# The earlier setup

These are the first studies, run on October 11 and 12, 2026, before the main setup in
[../experiments/](../experiments/). The main write-up compares the two setups in
[DETAILS.md, section 5](../DETAILS.md#the-earlier-setup).

Same model (gpt-6.1-sol), same reasoning effort ("low"), same kind of records and user messages. Two things
differ from the main setup:

- A coordinating agent inside Codex started each conversation as a new background agent. In the main setup a
  script starts one new Codex CLI process per conversation.
- The agent read the records by running a small command-line program (`client.py`). In the main setup it calls
  tools.

A **wrong answer** is a reply that gives the similar thing's fact and does not say whose it is.

## The studies

| Folder | What was compared | Conversations | Wrong answers |
|---|---|---:|---|
| [traces/company-quote-mixup/](traces/company-quote-mixup/README.md) | The company scenario: with the line "those are separate customer accounts" in the records, without it, and a first batch of ten | 30 | with the line 1 of 10; without it 4 of 10; first batch 2 of 10 |
| [traces/pharmacy-branch-mixup/](traces/pharmacy-branch-mixup/README.md) | The pharmacy scenario with three wordings of the search result | 29 | original listing 5 of 10; the two other wordings 0 of 10 and 0 of 9 |
| [traces/school-subscription-mixup/](traces/school-subscription-mixup/README.md) | The school scenario, nothing changed | 10 | 6 of 10 |
| [company-account-naming-20261012/](company-account-naming-20261012/README.md) | Company scenario: "our own" against the London company named in the question | 20 | 8 of 10 against 7 of 10 |
| [school-account-naming-20261012/](school-account-naming-20261012/README.md) | School scenario: "our own" against "our Westbrook School account's", after a check run of ten | 110 | 24 of 50 against 1 of 50; check run 3 of 10 |
| [pharmacy-answer-pressure-20261012/](pharmacy-answer-pressure-20261012/README.md) | Pharmacy scenario with and without "just the time, nothing else" | 100 | 14 of 50 against 0 of 50 |
| [school-answer-pressure-20261012/](school-answer-pressure-20261012/README.md) | "Which plan is our Westbrook School account on?" with and without "Just the plan, nothing else." | 100 | 0 of 50 against 0 of 50 |

The last row is a result with no mistake: when the question names the user's own school and asks for its plan,
the agent said that the plan is unknown in all 100 conversations.

## What was changed in these files after the runs

- Machine paths and Codex session ids are replaced with the placeholders `<tmp>`, `<workspace>`, `<codex-home>`
  and `<session>`. `<tmp-mistyped>` marks 33 places where the agent itself typed a wrong temporary folder name
  in a command.
- The manifests and audit files list a sha256 value per file. They were computed before the replacement, so
  they no longer match the files that contained a path or an id.
- Status notes and the coordinating agent's instruction files were removed. Every conversation is kept.
- The scripts are kept as a record. Seven of the 35 (`capture_observable.py`, one `analyze.py`, one
  `client-original.py`) contain a placeholder where a path was, so they do not run as they are.
