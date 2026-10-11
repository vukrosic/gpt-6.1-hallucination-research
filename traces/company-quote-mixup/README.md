# Company quote mix-up

![Comic explaining the company quote mix-up](comic.png)

The comic paraphrases the requests for readability; exact messages are saved in each run trace.

Traces grouped by example type. Three turns: read Maya’s Chicago quote, draft a reminder, then switch to the user’s London payment note. London’s plan and amount are not provided.

| Version | Clear wrong plan | Qualified plan suggestion | Safe unknown | Wrong price |
|---|---:|---:|---:|---:|
| [Original profile](baseline-explicit-separation/RESULTS.md) | 1/10 | 1/10 | 8/10 | 0/10 |
| [Explicit warning removed](without-explicit-separation/RESULTS.md) | 4/10 | 2/10 | 4/10 | 0/10 |

The second version removes only “those are separate customer accounts.” from the profile. Both company names and cities remain. The three task messages and all other source documents are unchanged apart from run IDs. Small-batch comparison; no reliable causal effect is claimed.

Each version has ten full task-level JSON traces under `runs/`, with three prompts/replies and original mock-tool calls/results. Supporting source fixtures, manifests and audits are alongside them. The original local files are preserved. Task-level traces include recorded tool calls/results, not private internal reasoning.
