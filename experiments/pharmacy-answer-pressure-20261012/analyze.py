"""Audit actual saved public traces and aggregate blinded decisions. No model calls."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
from math import comb, sqrt
from statistics import median
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def read(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def wilson(k, n):
    if not n: return None
    z = 1.959963984540054
    center = (k/n+z*z/(2*n))/(1+z*z/n)
    half = z*sqrt(k/n*(1-k/n)/n+z*z/(4*n*n))/(1+z*z/n)
    return [max(0, center-half), min(1, center+half)]

def fisher(a, n1, c, n2):
    if not n1 or not n2: return None
    k = a+c
    probabilities = {x: comb(n1,x)*comb(n2,k-x)/comb(n1+n2,k)
                     for x in range(max(0,k-n2), min(n1,k)+1)}
    observed = probabilities[a]
    return min(1.0, sum(p for p in probabilities.values() if p<=observed+1e-12))

def matched_exact(prevented, introduced):
    n = prevented+introduced
    return min(1.0, 2*sum(comb(n,i) for i in range(min(prevented,introduced)+1))/2**n) if n else 1.0

def json_objects(value):
    if isinstance(value, (dict,list)):
        yield value
        for child in (value.values() if isinstance(value,dict) else value): yield from json_objects(child)
    elif isinstance(value,str):
        seen = set()
        for text in [value.strip()]+value.splitlines():
            if text in seen or not text.startswith(('{','[')): continue
            seen.add(text)
            try: parsed = json.loads(text)
            except ValueError: continue
            if isinstance(parsed,(dict,list)): yield from json_objects(parsed)

def normalize_locator(prompt):
    match = re.search(r'Replace RUN_ID with ([A-Za-z0-9_-]+)\.', prompt)
    if not match: raise ValueError('No opaque run locator')
    return prompt.replace(match.group(1),'OPAQUE_RUN'), match.group(1)

def reported_usage(session_id):
    # Only numeric token metadata is extracted; never output raw native context.
    files = list(Path('/Users/vukrosic/.codex/sessions/2026/10/12').glob(f'*{session_id}*'))
    if len(files)!=1: return None
    usage = None
    for line in files[0].read_text().splitlines():
        row = json.loads(line)
        payload = row.get('payload',{})
        if row.get('type')=='event_msg' and payload.get('type')=='token_count':
            candidate = (payload.get('info') or {}).get('total_token_usage')
            if candidate:
                usage = {k:v for k,v in candidate.items() if isinstance(v,(int,float)) and not isinstance(v,bool)}
    return usage

def main():
    frozen = read(ROOT/'FROZEN.json')
    for file,key in [('PROTOCOL.json','protocol_sha256'),('SCHEDULE.json','schedule_sha256'),
                     ('FIXTURE.json','fixture_sha256'),('client.py','client_sha256')]:
        assert sha(ROOT/file)==frozen[key], file+' changed'
    protocol, schedule, fixture = read(ROOT/'PROTOCOL.json'),read(ROOT/'SCHEDULE.json'),read(ROOT/'FIXTURE.json')
    assert Counter(d['arm'] for d in schedule)=={'strict':50,'neutral':50}
    rows, audits, missing, unreviewed = [], [], [], []
    for d in schedule:
        rid = d['run_id']; directory = ROOT/'runs'/rid
        grade_path = ROOT/'reviews'/f'{rid}.json'
        if not (directory/'completion.json').exists(): missing.append(rid); continue
        if not grade_path.exists(): unreviewed.append(rid); continue
        grade, observable = read(grade_path), read(directory/'observable.json')
        completion, blinded = read(directory/'completion.json'), read(ROOT/'BLINDED'/f'{rid}.json')
        calls = [json.loads(line) for line in (directory/'client_calls.jsonl').read_text().splitlines() if line.strip()]
        issues = []
        runtime_rechecked = False
        if read(directory/'dispatch.json')!=d: issues.append('frozen dispatch changed')
        if observable['models']!=['gpt-6.1-sol']: issues.append('actual model mismatch')
        if observable['efforts']!=['low']: issues.append('actual effort mismatch')
        if blinded['actual_final_answers']!=observable['final_answers']: issues.append('blinded answer differs from native public trace')
        if len(observable['final_answers'])!=1: issues.append('not exactly one public final reply; preserve and inspect')
        if grade.get('input_sha256')!=sha(ROOT/'BLINDED'/f'{rid}.json'): issues.append('review input changed')
        if grade.get('condition_exposure') or grade.get('model')!='gpt-6.1-sol': issues.append('review provenance mismatch')
        if blinded['source_fixture']!=fixture: issues.append('blinded fixture differs')
        if not calls: issues.append('no actual client calls; inspect boundary/source visibility')
        objects = [obj for event in observable['observable_events']
                   if event['type'] in ('function_call_output','custom_tool_call_output')
                   for obj in json_objects(event.get('output'))]
        for call in calls:
            if call['response'] not in objects: issues.append('client response not completely visible in native public output')
            req, response = call['request'],call['response']; op=req.get('op')
            expected = None
            if op=='find_businesses': expected=fixture[op]
            if op=='get_business_page': expected=fixture[op] if req.get('business_id')==fixture[op]['business_id'] else {'error':'business_not_found'}
            if op=='place_call': expected=fixture[op] if req.get('phone_number')==fixture['get_business_page']['phone'] else {'connected':False,'detail':'Number unavailable.'}
            if expected is not None and expected!=response: issues.append('actual mock response differs from frozen service')
        # The successful attempt is identified by its public native path.
        attempt_matches=[]
        for ap in sorted((directory/'attempts').glob('a*/dispatch-actual.json')):
            attempt=read(ap)
            public=ap.parent/'observable.json'
            if public.exists() and read(public).get('agent_path')==observable['agent_path']: attempt_matches.append((ap,attempt))
        if len(attempt_matches)!=1: issues.append('successful actual dispatch not uniquely identified')
        else:
            ap,attempt=attempt_matches[0]
            prompt=attempt.get('prompt',attempt.get('intended_prompt',attempt.get('exact_prompt')))
            normalized,locator=normalize_locator(prompt)
            if normalized!=protocol['templates'][d['arm']]: issues.append('intended actual prompt changed beyond locator')
            for key,wanted in [('model','gpt-6.1-sol'),('effort','low'),('fork_turns','none')]:
                actual=attempt.get(key,attempt.get('reasoning_effort') if key=='effort' else None)
                if actual!=wanted: issues.append('actual requested '+key+' mismatch')
            runtime_path=Path(protocol['runtime_root'])/'mock_data'/f'{locator}.json'
            if runtime_path.exists():
                runtime_rechecked = True
                state=read(runtime_path)
                if state['fixture']!=fixture: issues.append('actual runtime fixture changed')
                if state['log']!=calls: issues.append('archived actual calls differ from runtime log')
        usage=reported_usage(observable['native_session_id'])
        if usage is not None: (directory/'reported-token-usage.json').write_text(json.dumps(usage,indent=2)+'\n')
        elif (directory/'reported-token-usage.json').exists():
            usage=read(directory/'reported-token-usage.json')
        answer='\n'.join(observable['final_answers'])
        row={'run_id':rid,'arm':d['arm'],'block':d['block'],'lane':d['lane'],
             'primary':grade['primary_unqualified_target_time'] is True,
             'disputed':grade['primary_unqualified_target_time'] is None,
             'strict':grade['strict_sensitivity_positive'],'category':grade['category'],
             'clarification':grade['clarification_requested'],'other_unsupported_claims':grade['other_unsupported_claims'],
             'answer':answer,'public_answer_characters':len(answer),'actual_mock_calls':len(calls),
             'latency_seconds':completion.get('latency_seconds'),'reported_token_usage':usage,
             'attempts':len(list((directory/'attempts').glob('a*/dispatch-actual.json'))),'audit_issues':sorted(set(issues))}
        rows.append(row);audits.append({'run_id':rid,'issues':row['audit_issues'],
                                      'runtime_rechecked':runtime_rechecked,
                                      'observable_sha256':sha(directory/'observable.json'),
                                      'client_calls_sha256':sha(directory/'client_calls.jsonl'),
                                      'review_sha256':sha(grade_path)})
    arms={}
    for arm in ['strict','neutral']:
        selected=[r for r in rows if r['arm']==arm];k=sum(r['primary'] for r in selected)
        times=[r['latency_seconds'] for r in selected if isinstance(r['latency_seconds'],(int,float))]
        arms[arm]={'n':len(selected),'unqualified_target_time':k,'rate':k/len(selected) if selected else None,
                   'wilson95':wilson(k,len(selected)),'strict_sensitivity':sum(r['strict'] for r in selected),
                   'disputed':sum(r['disputed'] for r in selected),'categories':dict(Counter(r['category'] for r in selected)),
                   'clarifications':sum(r['clarification'] for r in selected),
                   'median_latency_seconds':median(times) if times else None,
                   'median_public_answer_characters':median(r['public_answer_characters'] for r in selected) if selected else None,
                   'total_actual_mock_calls':sum(r['actual_mock_calls'] for r in selected),
                   'trials_with_reported_token_usage':sum(r['reported_token_usage'] is not None for r in selected)}
    blocks=defaultdict(dict)
    for r in rows: blocks[r['block']][r['arm']]=r
    pairs=[p for p in blocks.values() if len(p)==2]
    prevented=sum(p['strict']['primary'] and not p['neutral']['primary'] for p in pairs)
    introduced=sum(p['neutral']['primary'] and not p['strict']['primary'] for p in pairs)
    a,b=arms['strict'],arms['neutral']
    output={'updated_utc':datetime.now(timezone.utc).isoformat(),'planned':100,'complete_reviewed':len(rows),
            'complete':len(rows)==100,'missing_completed':missing,'completed_unreviewed':unreviewed,
            'audit_pass':all(not a['issues'] for a in audits),
            'runtime_rechecked_trials':sum(a['runtime_rechecked'] for a in audits),
            'arms':arms,'runs':rows,'audits':audits,
            'comparison':{'risk_difference_neutral_minus_strict':b['rate']-a['rate'] if a['n'] and b['n'] else None,
                          'fisher_two_sided_p':fisher(a['unqualified_target_time'],a['n'],b['unqualified_target_time'],b['n']),
                          'complete_matched_pairs':len(pairs),'discordant_prevented':prevented,'discordant_introduced':introduced,
                          'matched_exact_two_sided_p':matched_exact(prevented,introduced)},
            'extra_attempts_completed_logicals':sum(r['attempts']-1 for r in rows),
            'limits':['Single selected synthetic unanswerable case; not general hallucination rate.',
                      'This tests wording effect, not private reasoning or universal root cause.',
                      'Native incoming context is opaque; exact intended plaintext saved separately.',
                      'Separate same-family grader, blind to assigned arm but answerstyle can reveal it.',
                      'No historical pooling, no source-present utility controls in these100 runs.',
                      'Per-trial measured latency includes dispatch/queue where recorded; not parallel batch wall time.']}
    (ROOT/'ANALYSIS.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(f"{len(rows)}/100 complete and reviewed; audit={output['audit_pass']}")
    for arm,v in arms.items(): print(f"{arm}: {v['unqualified_target_time']}/{v['n']} unsupported; categories={v['categories']}")
    if not output['audit_pass']: print([a for a in audits if a['issues']])

if __name__=='__main__': main()
