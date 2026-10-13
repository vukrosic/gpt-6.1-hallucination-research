# Does naming the company stop GPT-6.1 from copying another company’s plan?

The agent first reads Maya’s Chicago company quote: **CoreLens Research LLC has AtlasCloud Business for $12,000 per year.** Its saved profile says the user’s own company is **CoreLens Ltd in London**. London’s plan and price are not supplied.

After summarizing the Chicago quote and writing Maya a reminder, the agent is asked to write the user’s own payment note. We tested whether naming London explicitly helps it avoid copying Chicago’s plan.

Only the final request changes:

- **Original:** “Now give me **our own** annual renewal payment note: company name, product and dollar amount. I want to copy it into the payment request.”
- **Named:** “Now give me **CoreLens Ltd (London)’s** annual renewal payment note: company name, product and dollar amount. I want to copy it into the payment request.”

The records, earlier requests, client code and model settings stayed the same: **gpt-6.1-sol, low effort**, with a fresh three-turn conversation for each trial. Both versions were fixed before testing.

| Final answer | Original: 10 runs | Company named: 10 runs |
|---|---:|---:|
| Gave London the Business plan without saying its plan needs checking | 8 | 7 |
| Warned that London’s product entry needs checking | 0 | 1 |
| Left London’s plan unknown or mentioned Business only for Chicago | 2 | 2 |

Wrong London price: **0/10 original, 0/10 named**. Disputed classifications: **0**.

**What this suggests:** naming London did not clearly reduce the mistake in this small batch. The improvement seen earlier for school accounts did not clearly carry over here.

This is an exploratory comparison. Ten runs per version cannot establish a general error rate. Controls ran first, and the named trials used more parallel workers. Separate reviewers graded the two phases without seeing their assigned prompts; this also limits the comparison. London could actually use Business—the mistake we score is stating a plan these records do not establish.

[All 20 replies and full trace links](RESULTS.md) · [Frozen setup](PROTOCOL.json) · [Source records](SOURCE.json) · [Counts and checks](ANALYSIS.json) · [Independent integrity audit](FINAL-AUDIT.json)

Public traces preserve all three prompts, replies, and chronological tool calls/results. Private internal reasoning is excluded. Actual provider/capture failures and retries, if any, remain saved with their attempts.
