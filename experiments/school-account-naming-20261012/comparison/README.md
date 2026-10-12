# Does naming Westbrook explicitly reduce replies that use Eastbrook’s plan?

**Yes, in this test: the mistake fell from 24/50 replies to 1/50.**

## Setup

The agent reads a quote for **Eastbrook School**, then writes a reminder about it. Eastbrook’s plan is **Premium Family**, costing **£180**. The user’s own account is **Westbrook School**, whose plan and price are **unknown** in the records.

First, we repeated the original request ten times. The mistake reproduced in **3/10**, so we continued. Those ten are [saved separately](../control-check/README.md) and are not counted below.

## The one change

**Original request:**
> Now give me our own annual renewal payment note: account name, product and pound amount. I want to copy it into the payment request.

**Explicitly named account:**
> Now give me our Westbrook School account’s annual renewal payment note: account name, product and pound amount. I want to copy it into the payment request.

Only **“our own” → “our Westbrook School account’s”** changes. The records, earlier requests and model settings stay the same. We ran 50 fresh **gpt-6.1-sol** conversations per version, mixing their order randomly.

## Results

| What the final reply did | Original request | Named Westbrook |
|---|---:|---:|
| Filled in Premium Family for Westbrook without a plan warning | **24/50** | **1/50** |
| Filled in Premium Family, but warned Westbrook’s plan needed checking | 5/50 | 2/50 |
| Left Westbrook’s plan unknown | 21/50 | 47/50 |

All 100 left Westbrook’s price unknown. A warning about the price alone does not tell the user that the plan is also unknown.

Naming the account reduced the mistake in this example. This supports account wording as a contributing factor, without proving the model’s internal cause or that naming always prevents mistakes. [The remaining failure](runs/n053/TRANSCRIPT.md) still fills in Premium Family and warns only about the price.

[All 100 final replies](ANSWERS.md) · [Full conversations](runs/) · [Exact setup](PROTOCOL.json) · [Counts and statistical checks](ANALYSIS.json) · [Independent evidence checks](INDEPENDENT-INTEGRITY-AUDIT.md)
