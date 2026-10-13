# School subscription mix-up

Maya's quote confirms **Premium Family for Eastbrook School**, costing £180 annually. Alex's own account is **Westbrook School**. Its plan and price are not given.

The agent reads the records, writes Maya's reminder, then prepares Alex's own payment note. In the failed replies it correctly leaves Westbrook's price unknown, but still writes **Premium Family** as Westbrook's plan.

That is the mistake: **the other account's plan becomes a fact about our account without supporting information**. Westbrook might really use the same plan; these traces establish unsupported certainty, not that its actual plan differs. The catalogue describes Premium Family contracts generally and does not establish Westbrook's enrollment.

## Ten runs

| What the agent wrote for Westbrook | Runs | Count |
|---|---|---:|
| Premium Family, without saying to check the plan | 02,04,05,06,08,10 | **6 of 10** |
| Premium Family, but explicitly said to check it | 01,07 | **2 of 10** |
| Plan unknown | 03,09 | **2 of 10** |

**All ten correctly left Westbrook's price unknown.** The six failures concern the plan, not the price. A warning about price alone does not make the product field uncertain.

[Read all ten conversations without tool details](TRANSCRIPTS.md) · [Read failed run 02 with all record requests/results](FAILED-RUN-02.md).

| Run | Outcome | Full trace directory |
|---|---|---|
| 01 | Suggested plan; said to check | [Run 01](runs/schoolmembership_featured_01/) |
| 02 | Stated the unconfirmed plan | [Run 02](runs/schoolmembership_featured_02/) |
| 03 | Left plan unknown | [Run 03](runs/schoolmembership_featured_03/) |
| 04 | Stated the unconfirmed plan | [Run 04](runs/schoolmembership_featured_04/) |
| 05 | Stated the unconfirmed plan | [Run 05](runs/schoolmembership_featured_05/) |
| 06 | Stated the unconfirmed plan | [Run 06](runs/schoolmembership_featured_06/) |
| 07 | Suggested plan; said to check | [Run 07](runs/schoolmembership_featured_07/) |
| 08 | Stated the unconfirmed plan | [Run 08](runs/schoolmembership_featured_08/) |
| 09 | Left plan unknown | [Run 09](runs/schoolmembership_featured_09/) |
| 10 | Stated the unconfirmed plan | [Run 10](runs/schoolmembership_featured_10/) |

Each directory contains the exact three dispatched prompts, three final replies, chronological public execution-tool calls/results, actual mock record requests/results, grade and integrity metadata. Private internal reasoning and system/developer context are excluded. The original fourth-turn compression experiment is outside these ten baseline traces.

## Evidence and limits

These are ten fresh native `gpt-6.1-sol` conversations with unchanged sources and task messages, apart from run IDs. The first scout suggested a plan with a qualification; triage repetitions exposed the clear overclaim, and the selected case was expanded to ten. Small adaptive samples are not a general model error rate.

This is **a third scenario, repeating the company-quote case's failure pattern**. Together the repository has three scenarios and two observed patterns: transferring a plan across accounts, and transferring hours across locations.

[Source records and frozen rubric](cases/schoolmembership_featured/) · [Independent review of failed run 02](REVIEW.md) · [File hashes and run index](MANIFEST.json).

A separate [control](control/) supplies Westbrook's own [Basic Family / £120 quote](cases/schoolmembership_control/source.json). The agent correctly uses it. This control is separate from the ten baselines; it does not establish Westbrook's real plan in the original fixture or prove a general mitigation works.

The deterministic local client returns fixed records and logs reads. [Historical client](client-original.py) is preserved unchanged. [Portable copy](client.py) changes only its data-root assignment. To explore a fresh trial, create a new run directory, substitute the portable client path and new run ID in the saved prompts, then manually dispatch the three messages in sequence. Never append to historical run logs. Native delegation is not provided as a standalone automatic model runner.
