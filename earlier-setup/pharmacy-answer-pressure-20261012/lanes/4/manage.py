from pathlib import Path
import json,sys,datetime,hashlib,shutil
sys.path.insert(0,str(Path.cwd()))
from capture_observable import capture
p=Path.cwd();s=json.loads((p/'lanes/4/SCHEDULE.json').read_text());now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def status():
 completed=[];live=[];unstarted=[];attempts={}
 for r in s:
  rid=r['run_id'];rp=p/'runs'/rid;ats=sorted((rp/'attempts').glob('a*')) if (rp/'attempts').exists() else [];a=ats[-1] if ats else rp/'attempts/a1'
  if (rp/'completion.json').exists(): completed.append(rid)
  elif (a/'dispatch-actual.json').exists():live.append({'run_id':rid,'handle':'/root/assistant_batch4/'+rid+'_'+a.name})
  else:unstarted.append(rid)
  if a.exists():attempts[rid]=[z.name for z in ats]
 (p/'lanes/4/STATUS.json').write_text(json.dumps({'updated_utc':now(),'completed_ids':completed,'live_handles':live,'unstarted_ids':unstarted,'attempts':attempts,'actual_terminal_errors':[json.loads(f.read_text()) for r in s for f in (p/'runs'/r['run_id']/'attempts').glob('*/terminal.json') if json.loads(f.read_text()).get('status')=='failed'],'max_active':1},indent=2)+'\n')
for rid in sys.argv[2:]:
 r=next(r for r in s if r['run_id']==rid);ats=sorted((p/'runs'/rid/'attempts').glob('a*'));a=ats[-1] if ats else p/'runs'/rid/'attempts/a1';a.mkdir(parents=True,exist_ok=True)
 if sys.argv[1]=='dispatch':
  (a/'dispatch-actual.json').write_text(json.dumps({**r,'dispatch_utc':now(),'attempt':'a1','locator':rid},indent=2)+'\n');print(r['prompt'])
 if sys.argv[1]=='complete':
  o=capture('/root/assistant_batch4/'+rid+'_'+a.name);(a/'observable.json').write_text(json.dumps(o,indent=2)+'\n')
  raw=json.loads((Path(r['runtime_root'])/'mock_data'/f"{json.loads((a/'dispatch-actual.json').read_text()).get('locator',rid)}.json").read_text());logs=raw.get('log',[])
  (a/'client_calls.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in logs))
  d=json.loads((a/'dispatch-actual.json').read_text());t=now();lat=(datetime.datetime.fromisoformat(t)-datetime.datetime.fromisoformat(d['dispatch_utc'])).total_seconds()
  result={'status':'completed','completed_utc':t,'attempt':a.name,'agent_path':o['agent_path'],'models':o['models'],'efforts':o['efforts'],'latency_seconds':lat,'fixture_sha256':r['source_sha256'],'final_answer_count':len(o['final_answers']),'empty_reply':not any(o['final_answers']),'incoming_plaintext_verified':False}
  (a/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
  for f in ['observable.json','client_calls.jsonl']:shutil.copyfile(a/f,p/'runs'/rid/f)
  (p/'runs'/rid/'completion.json').write_text(json.dumps(result,indent=2)+'\n')
  b=p/'BLINDED';b.mkdir(exist_ok=True)
  (b/f'{rid}.json').write_text(json.dumps({'logical_run_id':rid,'source_fixture':json.loads((p/'FIXTURE.json').read_text()),'source_sha256':r['source_sha256'],'actual_final_answers':o['final_answers'],'model':o['models'],'effort':o['efforts'],'requested_situation':'Baywell pharmacy on Castro closing tonight, Monday12October2026,09:15SanFrancisco'},indent=2)+'\n')
  transcript='# Exact intended initial prompt\n\n'+d['prompt']+'\n\n# Chronological public events\n\n'+'\n\n'.join(json.dumps(x,ensure_ascii=False,indent=2) for x in o['observable_events'])
  (p/'runs'/rid/'TRANSCRIPT.md').write_text(transcript+'\n')
  (a/'HASHES.json').write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in a.iterdir() if f.is_file() and f.name!='HASHES.json'},indent=2)+'\n')
  print(rid,len(logs),len(o['final_answers']))
status()
