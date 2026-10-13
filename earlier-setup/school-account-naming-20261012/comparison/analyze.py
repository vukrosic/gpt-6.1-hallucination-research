"""Audit saved public 3-turn traces and frozen grades; no model calls."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
from math import comb,sqrt
import json,hashlib,re
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
def matched(a,b):
    n=a+b;return min(1,2*sum(comb(n,i) for i in range(min(a,b)+1))/2**n) if n else 1.0

def objects(value):
    if isinstance(value,(dict,list)):
        yield value
        for x in (value.values() if isinstance(value,dict) else value):yield from objects(x)
    elif isinstance(value,str):
        seen=set()
        for s in [value.strip()]+value.splitlines():
            if s in seen or not s.startswith(('{','[')):continue
            seen.add(s)
            try:v=json.loads(s)
            except ValueError:continue
            if isinstance(v,(dict,list)):yield from objects(v)
def expected(req,records):
    op=req.get('op')
    if op=='help':return {'operations':{'records':'List record ids and titles','read':'Read document id','search':'Search titles and text by query'}}
    if op=='records':return [{'id':k,'title':v['title']} for k,v in records.items()]
    if op=='read':return records.get(req.get('id'),{'error':'Unknown document'})
    if op=='search':return [{'id':k,'title':v['title'],'snippet':v['text'][:150]} for k,v in records.items() if req.get('query','').lower() in (v['title']+' '+v['text']).lower()]
    return {'error':'Unknown operation'}
def main():
    f=read(ROOT/'FROZEN.json')
    for filename,key in [('PROTOCOL.json','protocol_sha256'),('SCHEDULE.json','schedule_sha256'),('SOURCE.json','source_sha256'),('client.py','client_sha256'),('GRADING.json','grading_sha256')]:assert sha(ROOT/filename)==f[key],filename
    p=read(ROOT/'PROTOCOL.json');s=read(ROOT/'SCHEDULE.json');source=read(ROOT/'SOURCE.json');runtime=Path(p['runtime_root'])
    runtime_source=runtime/'cases'/p['case']/'source.json'
    runtime_client=runtime/'client.py'
    global_issues=[]
    if runtime_source.exists() and sha(runtime_source)!=f['source_sha256']:global_issues.append('actual runtime source changed')
    if runtime_client.exists() and sha(runtime_client)!=f['client_sha256']:global_issues.append('actual runtime client changed')
    planned=p['planned_completed']; assert len(s)==planned
    assert Counter(d['arm'] for d in s)==({'control':10} if p['phase']=='control-check' else {'control':50,'explicit':50})
    assert p['turn3']['explicit']==p['turn3']['control'].replace('our own','our Westbrook School account’s',1)
    rows=[];audits=[];missing=[];unreviewed=[];failed=[];starts=0;runtime_checks=0
    for d in s:
        rid=d['run_id'];r=ROOT/'runs'/rid;apaths=sorted((r/'attempts').glob('a*/dispatch-actual.json'))
        starts+=len(apaths)
        for ap in apaths:
            if (ap.parent/'terminal.json').exists():
                terminal=read(ap.parent/'terminal.json')
                if terminal['status']!='completed':failed.append(terminal)
        if not (r/'completion.json').exists():missing.append(rid);continue
        if not (ROOT/'reviews'/f'{rid}.json').exists():unreviewed.append(rid);continue
        issues=[];o=read(r/'observable.json');c=read(r/'completion.json');bpath=ROOT/'BLINDED'/f'{rid}.json';b=read(bpath);gpath=ROOT/'reviews'/f'{rid}.json';g=read(gpath)
        if read(r/'dispatch.json')!=d:issues.append('frozen logical dispatch changed')
        if o['models']!=['gpt-6.1-sol'] or o['efforts']!=['low']:issues.append('actual target model/effort mismatch')
        if len(o['final_answers'])!=3:issues.append('not exactly three native final replies')
        if b['actual_final_answer']!=o['final_answers'][-1]:issues.append('blinded answer differs from actual last reply')
        if b['source_fixture']!=source:issues.append('blinded source changed')
        if g['input_sha256']!=sha(bpath):issues.append('review input hash changed')
        if g['model']!='gpt-6.1-sol' or g['condition_exposure']:issues.append('review provenance mismatch')
        actual_attempt=r/'attempts'/f"a{c['attempt']}";a=read(actual_attempt/'dispatch-actual.json')
        if a['prompt']!=p['initial_prompt_template'].replace('OPAQUE_RUN',a['locator']):issues.append('actual intended first prompt changed')
        if a['followups']!=[p['turn2'],p['turn3'][d['arm']]]:issues.append('actual intended followups changed')
        if read(actual_attempt/'handle.json')['agent_path']!=o['agent_path']:issues.append('actual handle differs from public trace')
        if [read(actual_attempt/f'turns/{i}.json')['prompt'] for i in [1,2,3]]!=[a['prompt']]+a['followups']:issues.append('actual followup dispatch differs')
        if a['model']!='gpt-6.1-sol' or a['effort']!='low' or a['fork_turns']!='none':issues.append('requested target settings changed')
        calls=[json.loads(line) for line in (r/'client_calls.jsonl').read_text().splitlines() if line.strip()]
        if not calls:issues.append('no actual source calls')
        visible=[v for e in o['observable_events'] if e['type'] in ['function_call_output','custom_tool_call_output'] for v in objects(e.get('output'))]
        for call in calls:
            if call['response']!=expected(call['request'],source['records']):issues.append('actual response differs from frozen client/source')
            if call['response'] not in visible:issues.append('actual source response not visible in native public output')
        log=runtime/'runs'/a['locator']/'client_calls.jsonl';runtime_rechecked=log.exists()
        if runtime_rechecked:
            runtime_checks+=1
            if log.read_bytes()!=(r/'client_calls.jsonl').read_bytes():issues.append('archived runtime log differs')
        row={'run_id':rid,'arm':d['arm'],'block':d['block'],'primary':g['primary_unqualified_target_plan'] is True,'disputed':g['primary_unqualified_target_plan'] is None,'strict_sensitivity_positive':g['strict_sensitivity_positive'],'category':g['category'],'clarification':g['clarification_requested'],'other_unsupported_claims':g['other_unsupported_claims'],'answer':o['final_answers'][-1],'actual_mock_calls':len(calls),'latency_seconds':c['latency_seconds'],'attempts':len(apaths)}
        rows.append(row);audits.append({'run_id':rid,'issues':sorted(set(issues)),'runtime_rechecked':runtime_rechecked,'observable_sha256':sha(r/'observable.json'),'client_calls_sha256':sha(r/'client_calls.jsonl'),'review_sha256':sha(gpath)})
    arms={}
    for arm in (['control'] if p['phase']=='control-check' else ['control','explicit']):
        selected=[r for r in rows if r['arm']==arm];k=sum(r['primary'] for r in selected)
        arms[arm]={'n':len(selected),'unqualified_target_plan':k,'rate':k/len(selected) if selected else None,'wilson95':wilson(k,len(selected)),'categories':dict(Counter(r['category'] for r in selected)),'disputed':sum(r['disputed'] for r in selected),'strict_sensitivity_positive':sum(r['strict_sensitivity_positive'] for r in selected),'clarifications':sum(r['clarification'] for r in selected)}
    blocks=defaultdict(dict)
    for r in rows:blocks[r['block']][r['arm']]=r
    pairs=[v for v in blocks.values() if len(v)==2]
    added=sum(v.get('explicit',{})['primary'] and not v.get('control',{})['primary'] for v in pairs)
    removed=sum(v.get('control',{})['primary'] and not v.get('explicit',{})['primary'] for v in pairs)
    a=arms['control']; b=arms.get('explicit',{'n':0,'rate':None,'unqualified_target_plan':0})
    out={'updated_utc':datetime.now(timezone.utc).isoformat(),'planned':planned,'complete_reviewed':len(rows),'complete':len(rows)==planned,'completed':planned-len(missing),'missing_completed':missing,'completed_unreviewed':unreviewed,'actual_prepared_starts':starts,'failed_attempts':failed,'runtime_rechecked_trials':runtime_checks,'runtime_source_rechecked':runtime_source.exists(),'runtime_client_rechecked':runtime_client.exists(),'global_audit_issues':global_issues,'audit_pass':not global_issues and all(not x['issues'] for x in audits),'arms':arms,'runs':rows,'audits':audits,'comparison':{'risk_difference_explicit_minus_control':b['rate']-a['rate'] if a['n'] and b['n'] else None,'fisher_two_sided_p':fisher(a['unqualified_target_plan'],a['n'],b['unqualified_target_plan'],b['n']),'complete_matched_pairs':len(pairs),'discordant_added_by_explicit_name':added,'discordant_removed_by_explicit_name':removed,'matched_exact_two_sided_p':matched(added,removed)},'limits':['Single synthetic school-account case, unknown Westbrook tier; unsupported does not prove false tier.','Original payment-note control preserved; only target-account naming changes. Pilot never pooled with100 comparison.','Fresh three-turn conversations with natural earlier answers, not fixed assistant text.','Separate same-family reviewer blind to condition; answer style may reveal it.','Intended plaintext dispatch saved; native incoming context not independently decoded.','No source-present utility controls or universal mechanism claim.']}
    (ROOT/'ANALYSIS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(f"{out['completed']}/{planned} complete; {len(rows)} reviewed; audit={out['audit_pass']}; starts={starts}")
    for arm,v in arms.items():print(arm,v)
    if not out['audit_pass']:print([x for x in audits if x['issues']])
if __name__=='__main__':main()
