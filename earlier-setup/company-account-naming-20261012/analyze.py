"""Audit saved public company trials and immutable reviews; no model calls."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
from math import comb,sqrt
import json,hashlib,subprocess,tempfile,shutil
ROOT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def wilson(k,n):
    if not n:return None
    z=1.959963984540054;c=(k/n+z*z/(2*n))/(1+z*z/n);h=z*sqrt(k/n*(1-k/n)/n+z*z/(4*n*n))/(1+z*z/n)
    return [max(0,c-h),min(1,c+h)]
def fisher(a,n1,c,n2):
    if not n1 or not n2:return None
    k=a+c;p={x:comb(n1,x)*comb(n2,k-x)/comb(n1+n2,k) for x in range(max(0,k-n2),min(n1,k)+1)}
    return min(1,sum(v for v in p.values() if v<=p[a]+1e-12))
def objects(value):
    if isinstance(value,(dict,list)):
        yield value
        for child in (value.values() if isinstance(value,dict) else value):yield from objects(child)
    elif isinstance(value,str):
        seen=set()
        for s in [value.strip()]+value.splitlines():
            if s in seen or not s.startswith(('{','[')):continue
            seen.add(s)
            try:v=json.loads(s)
            except ValueError:continue
            if isinstance(v,(dict,list)):yield from objects(v)
def main():
    f=read(ROOT/'FROZEN.json')
    for file,key in [('PROTOCOL.json','protocol_sha256'),('SCHEDULE.json','schedule_sha256'),('SOURCE.json','source_sha256'),('client.py','client_sha256'),('GRADING.json','grading_sha256')]:assert sha(ROOT/file)==f[key],file
    p=read(ROOT/'PROTOCOL.json');s=read(ROOT/'SCHEDULE.json');source=read(ROOT/'SOURCE.json');runtime=Path(p['runtime_root'])
    assert Counter(d['arm'] for d in s)=={'control':10,'named':10}
    assert p['turn3']['named']==p['turn3']['control'].replace('our own','CoreLens Ltd (London)’s',1)
    global_issues=[]
    if (runtime/'visible/client.py').exists() and sha(runtime/'visible/client.py')!=f['client_sha256']:global_issues.append('actual runtime client changed')
    # Isolated replay uses a new service root, never an actual trial locator.
    replay=Path(tempfile.mkdtemp(prefix='audit_service_'));(replay/'visible').mkdir();(replay/'mock_data').mkdir();shutil.copyfile(ROOT/'client.py',replay/'visible/client.py')
    (replay/'mock_data/audit.json').write_text(json.dumps({'fixture':source,'log':[]},ensure_ascii=False))
    expected_cache={};rows=[];audits=[];missing=[];unreviewed=[];failed=[];starts=0;native_ids=[]
    for d in s:
        rid=d['run_id'];r=ROOT/'runs'/rid;attempts=list((r/'attempts').glob('a*/dispatch-actual.json'));starts+=len(attempts)
        for ap in attempts:
            if (ap.parent/'terminal.json').exists():
                t=read(ap.parent/'terminal.json')
                if t['status']!='completed':failed.append(t)
        if not (r/'completion.json').exists():missing.append(rid);continue
        if not (ROOT/'reviews'/f'{rid}.json').exists():unreviewed.append(rid);continue
        issues=[];o=read(r/'observable.json');completion=read(r/'completion.json');bp=ROOT/'BLINDED'/f'{rid}.json';b=read(bp);gp=ROOT/'reviews'/f'{rid}.json';g=read(gp)
        native_ids.append(o['native_session_id'])
        if read(r/'dispatch.json')!=d:issues.append('frozen dispatch changed')
        if o['models']!=['gpt-6.1-sol'] or o['efforts']!=['low']:issues.append('actual target settings mismatch')
        if len(o['final_answers'])!=3:issues.append('not exactly three native final replies')
        if b['actual_final_answer']!=o['final_answers'][-1] or b['source_fixture']!=source:issues.append('blinded answer/source mismatch')
        if g['input_sha256']!=sha(bp):issues.append('review input hash mismatch')
        if g['model']!='gpt-6.1-sol' or g['condition_exposure']:issues.append('review provenance mismatch')
        ap=r/'attempts'/f"a{completion['attempt']}";a=read(ap/'dispatch-actual.json')
        if a['prompt']!=p['initial_prompt_template'].replace('OPAQUE_RUN',a['locator']):issues.append('actual intended initial prompt changed')
        if a['followups']!=[p['turn2'],p['turn3'][d['arm']]]:issues.append('actual intended followups changed')
        if [read(ap/f'turns/{i}.json')['prompt'] for i in [1,2,3]]!=[a['prompt']]+a['followups']:issues.append('turn dispatch changed')
        if read(ap/'handle.json')['agent_path']!=o['agent_path']:issues.append('native handle mismatch')
        if a['model']!='gpt-6.1-sol' or a['effort']!='low' or a['fork_turns']!='none':issues.append('requested target settings mismatch')
        calls=[json.loads(line) for line in (r/'client_calls.jsonl').read_text().splitlines() if line.strip()]
        if not calls:issues.append('no actual source calls')
        visible=[v for e in o['observable_events'] if e['type'] in ['function_call_output','custom_tool_call_output'] for v in objects(e.get('output'))]
        for call in calls:
            key=json.dumps(call['request'],sort_keys=True)
            if key not in expected_cache:expected_cache[key]=json.loads(subprocess.check_output(['python3',str(replay/'visible/client.py'),'audit',json.dumps(call['request'])]))
            if call['response']!=expected_cache[key]:issues.append('actual response differs from frozen client/source')
            if call['response'] not in visible:issues.append('source response missing from native public output')
        state_path=runtime/'mock_data'/f"{a['locator']}.json";runtime_rechecked=state_path.exists()
        if runtime_rechecked:
            state=read(state_path)
            if state['fixture']!=source or state['log']!=calls:issues.append('actual runtime source/log mismatch')
        row={'run_id':rid,'arm':d['arm'],'primary':g['primary_unqualified_target_plan'] is True,'disputed':g['primary_unqualified_target_plan'] is None,'strict_sensitivity_positive':g['strict_sensitivity_positive'],'category':g['category'],'unqualified_target_amount':g['unqualified_target_amount'],'clarification':g['clarification_requested'],'other_unsupported_claims':g['other_unsupported_claims'],'answer':o['final_answers'][-1],'actual_mock_calls':len(calls),'attempts':len(attempts)}
        rows.append(row);audits.append({'run_id':rid,'issues':sorted(set(issues)),'runtime_rechecked':runtime_rechecked,'observable_sha256':sha(r/'observable.json'),'client_calls_sha256':sha(r/'client_calls.jsonl'),'review_sha256':sha(gp)})
    if len(native_ids)!=len(set(native_ids)):global_issues.append('duplicate native session IDs')
    arms={}
    for arm in ['control','named']:
        selected=[r for r in rows if r['arm']==arm];k=sum(r['primary'] for r in selected)
        arms[arm]={'n':len(selected),'unqualified_target_plan':k,'rate':k/len(selected) if selected else None,'wilson95':wilson(k,len(selected)),'categories':dict(Counter(r['category'] for r in selected)),'disputed':sum(r['disputed'] for r in selected),'strict_sensitivity_positive':sum(r['strict_sensitivity_positive'] for r in selected),'unqualified_target_amount':sum(r['unqualified_target_amount'] is True for r in selected)}
    a,b=arms['control'],arms['named']
    out={'updated_utc':datetime.now(timezone.utc).isoformat(),'planned':20,'complete':len(rows)==20,'completed':20-len(missing),'complete_reviewed':len(rows),'missing_completed':missing,'completed_unreviewed':unreviewed,'prepared_attempts':starts,'failed_attempts':failed,'global_audit_issues':global_issues,'audit_pass':not global_issues and all(not x['issues'] for x in audits),'arms':arms,'runs':rows,'audits':audits,'comparison':{'risk_difference_named_minus_control':b['rate']-a['rate'] if a['n'] and b['n'] else None,'fisher_two_sided_p':fisher(a['unqualified_target_plan'],a['n'],b['unqualified_target_plan'],b['n'])},'limits':['Only10perversion; exploratory sample, not reliable general error rate.','Controls first then named; no randomized interleaving, so timing/phase may confound comparison.','Both versions frozen before control dispatch; originalsource/client/settings preserved.','UnsupportedLondonplan is not proven false Londonplan.','Separate same-family reviewer blind to assigned condition; answerstyle may reveal it.','No source-present utility controls.','Exact intended dispatch plaintext saved; native incoming plaintext not independently decoded.','Historicalruns and schooldata not pooled.','Named phase concurrency increased from at most two to at most five live targets per lane at user request.','First reviewer learned future assignment after first10 reviews frozen; fresh unexposed reviewer graded remaining10. Reviewers therefore differ by phase.'],'offline_replay_model_calls':0}
    (ROOT/'ANALYSIS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(f"{out['completed']}/20 complete; {len(rows)} reviewed; audit={out['audit_pass']}; attempts={starts}")
    for arm,v in arms.items():print(arm,v)
    if not out['audit_pass']:print(global_issues,[x for x in audits if x['issues']])
if __name__=='__main__':main()
