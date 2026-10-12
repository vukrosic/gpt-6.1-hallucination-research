import json,hashlib,re,importlib.util,datetime
from pathlib import Path
from collections import Counter
p=json.loads(Path('PROTOCOL.json').read_text());s=json.loads(Path('SCHEDULE.json').read_text());f=json.loads(Path('FIXTURE.json').read_text());fz=json.loads(Path('FROZEN.json').read_text());issues=[];sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
for file,key in [('PROTOCOL.json','protocol_sha256'),('SCHEDULE.json','schedule_sha256'),('FIXTURE.json','fixture_sha256'),('client.py','client_sha256')]:
 if sha(file)!=fz[key]:issues.append(f'{file}: frozen hash mismatch')
if sha(Path(p['runtime_root'])/'visible/client.py')!=fz['client_sha256']:issues.append('Runtime client hash mismatch')
normalize=lambda q:re.sub(r'Replace RUN_ID with [A-Za-z0-9_-]+\.', 'Replace RUN_ID with OPAQUE_RUN.',q)
if p['templates']['strict']!=p['templates']['neutral']+' just the time, nothing else':issues.append('Template semantic change differs')
completed=[];pending=[];retry=[];failed=[];all_attempts=0;logs=0;artifacts_pending=[]
spec=importlib.util.spec_from_file_location('a','analyze.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
for d in s:
 rid=d['run_id'];rd=Path('runs')/rid
 if json.loads((rd/'dispatch.json').read_text())!=d:issues.append(rid+': frozen run dispatch mismatch')
 if normalize(d['prompt'])!=p['templates'][d['arm']]:issues.append(rid+': frozen prompt mismatch')
 aps=sorted((rd/'attempts').glob('a*/dispatch-actual.json'));all_attempts+=len(aps);successful=0
 if len(aps)>2:issues.append(rid+': more than two starts')
 if len(aps)>1:retry.append(rid)
 for ap in aps:
  di=json.loads(ap.read_text());q=di.get('prompt',di.get('intended_prompt',di.get('exact_prompt')))
  if normalize(q)!=p['templates'][d['arm']]:issues.append(str(ap)+': prompt mismatch')
  for key,want in [('model','gpt-6.1-sol'),('effort','low'),('fork_turns','none')]:
   val=di.get(key,di.get('reasoning_effort') if key=='effort' else None)
   if val!=want:issues.append(str(ap)+': requested '+key+' mismatch')
  locator=re.search(r'Replace RUN_ID with ([A-Za-z0-9_-]+)\.',q).group(1);state=json.loads((Path(p['runtime_root'])/'mock_data'/f'{locator}.json').read_text())
  if state['fixture']!=f:issues.append(str(ap)+': runtime fixture mismatch')
  op=ap.parent/'observable.json';cp=ap.parent/'client_calls.jsonl'
  if not op.exists():continue
  o=json.loads(op.read_text())
  if o['models']!=['gpt-6.1-sol'] or o['efforts']!=['low']:issues.append(str(op)+': observed settings mismatch')
  if o['final_answers']:successful+=1
  else:failed.append(rid)
  for event in o['observable_events']:
   if event['type'] not in ['function_call','function_call_output','custom_tool_call','custom_tool_call_output','assistant_message']:issues.append(str(op)+': unexpected event type')
   if event['type']=='assistant_message' and event['channel'] not in ['final','commentary']:issues.append(str(op)+': private assistant channel')
  if cp.exists():
   calls=[json.loads(x) for x in cp.read_text().splitlines() if x.strip()];logs+=len(calls)
   if calls!=state['log']:issues.append(str(cp)+': runtime logs differ')
   objects=[obj for e in o['observable_events'] if e['type'] in ['function_call_output','custom_tool_call_output'] for obj in a.json_objects(e.get('output'))]
   for call in calls:
    if call['response'] not in objects:issues.append(str(cp)+': logged response absent from public trace')
  if len(o['final_answers'])>1:issues.append(str(op)+': multiple replies')
 if successful>1:issues.append(rid+': successful reply repeated')
 if (rd/'completion.json').exists():
  completed.append(rid);op=rd/'observable.json';bp=Path('BLINDED')/f'{rid}.json'
  if not op.exists() or not bp.exists():artifacts_pending.append(rid);continue
  o=json.loads(op.read_text());b=json.loads(bp.read_text())
  if b['actual_final_answers']!=o['final_answers'] or b['source_fixture']!=f:issues.append(rid+': blinded evidence mismatch')
  if any(k in b for k in ['arm','prompt','initialprompt','schedule','hypothesis']):issues.append(rid+': blinded direct exposure')
 else:pending.append(rid)
assert abs(a.fisher(0,10,0,10)-1)<1e-12
assert abs(a.fisher(10,10,0,10)-2/184756)<1e-12
assert a.matched_exact(0,0)==1 and abs(a.matched_exact(5,0)-.0625)<1e-12
assert abs(a.fisher(3,10,1,10)-a.fisher(1,10,3,10))<1e-12
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),completed_count=len(completed),pending_ids=pending,artifacts_pending=artifacts_pending,attempt_dispatches=all_attempts,retried_ids=retry,no_final_attempt_ids=failed,logged_calls=logs,issues=issues,arm_counts=dict(Counter(x['arm'] for x in s)))
Path('lanes/3/INDEPENDENT-AUDIT-SNAPSHOT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
