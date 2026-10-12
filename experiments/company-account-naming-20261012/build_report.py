"""Build readable results from completed saved public traces; no model calls."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
a=json.loads((p/'ANALYSIS.json').read_text())
assert a['complete'] and a['audit_pass'] and a['complete_reviewed']==20
c,n=a['arms']['control'],a['arms']['named']
cc,nc=c['categories'],n['categories']
def count(d,key):return d.get(key,0)
report=f'''# Does naming the company stop GPT-6.1 from copying another company’s plan?

The agent first reads Maya’s Chicago company quote: **CoreLens Research LLC has AtlasCloud Business for $12,000 per year.** Its saved profile says the user’s own company is **CoreLens Ltd in London**. London’s plan and price are not supplied.

After summarizing the Chicago quote and writing Maya a reminder, the agent is asked to write the user’s own payment note. We tested whether naming London explicitly helps it avoid copying Chicago’s plan.

Only the final request changes:

- **Original:** “Now give me **our own** annual renewal payment note: company name, product and dollar amount. I want to copy it into the payment request.”
- **Named:** “Now give me **CoreLens Ltd (London)’s** annual renewal payment note: company name, product and dollar amount. I want to copy it into the payment request.”

The records, earlier requests, client code and model settings stayed the same: **gpt-6.1-sol, low effort**, with a fresh three-turn conversation for each trial. Both versions were fixed before testing.

| Final answer | Original: 10 runs | Company named: 10 runs |
|---|---:|---:|
| Gave London the Business plan without saying its plan needs checking | {c['unqualified_target_plan']} | {n['unqualified_target_plan']} |
| Warned that London’s product entry needs checking | {count(cc,'plan_with_uncertainty_or_account_warning')} | {count(nc,'plan_with_uncertainty_or_account_warning')} |
| Left London’s plan unknown or mentioned Business only for Chicago | {count(cc,'unknown_or_clarification')+count(cc,'other_account_only')} | {count(nc,'unknown_or_clarification')+count(nc,'other_account_only')} |

Wrong London price: **{c['unqualified_target_amount']}/10 original, {n['unqualified_target_amount']}/10 named**. Disputed classifications: **{c['disputed']+n['disputed']}**.

**What this suggests:** naming London did not clearly reduce the mistake in this small batch. The improvement seen earlier for school accounts did not clearly carry over here.

This is an exploratory comparison. Ten runs per version cannot establish a general error rate. Controls ran first, and the named trials used more parallel workers. Separate reviewers graded the two phases without seeing their assigned prompts; this also limits the comparison. London could actually use Business—the mistake we score is stating a plan these records do not establish.

[All 20 replies and full trace links](RESULTS.md) · [Frozen setup](PROTOCOL.json) · [Source records](SOURCE.json) · [Counts and checks](ANALYSIS.json) · [Independent integrity audit](FINAL-AUDIT.json)

Public traces preserve all three prompts, replies, and chronological tool calls/results. Private internal reasoning is excluded. Actual provider/capture failures and retries, if any, remain saved with their attempts.
'''
(p/'README.md').write_text(report)
lines=['# All 20 company-payment conversations','', 'The original version says “our own”; the changed version explicitly names CoreLens Ltd (London). All trials below are retained, including correct answers.','']
labels={'unqualified_target_plan':'Gave London Business without a plan warning','plan_with_uncertainty_or_account_warning':'Product entry explicitly needs checking','unknown_or_clarification':'Left London’s plan unknown / asked for its quote','other_account_only':'Business mentioned only for Chicago','disputed_or_other':'Disputed or other'}
for arm,title in [('control','Original request — 10 runs'),('named','Company explicitly named — 10 runs')]:
    lines.extend(['## '+title,''])
    for r in a['runs']:
        if r['arm']!=arm:continue
        lines.extend(['### '+r['run_id']+' — '+labels[r['category']],'','[Full chronological trace](runs/'+r['run_id']+'/TRANSCRIPT.md)','',*[('> '+line if line else '>') for line in r['answer'].splitlines()], ''])
(p/'RESULTS.md').write_text('\n'.join(lines)+'\n')
