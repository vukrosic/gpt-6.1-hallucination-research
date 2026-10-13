from pathlib import Path
import json,sys,datetime,hashlib,shutil
sys.path.insert(0,str(Path.cwd()))
from capture_observable import capture
s=json.loads(Path('lanes/3/SCHEDULE.json').read_text()); now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
mode=sys.argv[1];ids=sys.argv[2:]
for rid in ids:
 d=next(x for x in s if x['run_id']==rid);a=Path('runs')/rid/'attempts/a1';a.mkdir(parents=True,exist_ok=True)
 if mode=='prepare':
  (a/'dispatch-actual.json').write_text(json.dumps(dict(d,dispatch_utc=now(),attempt=1),indent=2)+'\n')
 elif mode=='finish':
  h=json.loads((a/'handle.json').read_text());o=capture(h['agent_path']);(a/'observable.json').write_text(json.dumps(o,indent=2)+'\n');f=Path(d['runtime_root'])/'mock_data'/f'{rid}.json';data=json.loads(f.read_text());(a/'client_calls.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in data.get('log',[])))
  dis=json.loads((a/'dispatch-actual.json').read_text());elapsed=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(dis['dispatch_utc'])).total_seconds()
  c=dict(logical_run_id=rid,status='completed',attempt=1,agent_path=h['agent_path'],model=o['models'],effort=o['efforts'],completed_utc=now(),latency_seconds=elapsed,source_sha256=d['source_sha256'],fixture_runtime_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),final_answer_count=len(o['final_answers']),incoming_plaintext_verified=False)
  (a/'terminal.json').write_text(json.dumps(c,indent=2)+'\n');(Path('runs')/rid/'completion.json').write_text(json.dumps(c,indent=2)+'\n')
  for name in ['observable.json','client_calls.jsonl']:shutil.copyfile(a/name,Path('runs')/rid/name)
  b=dict(logical_run_id=rid,source_fixture=json.loads(Path('FIXTURE.json').read_text()),source_sha256=d['source_sha256'],actual_final_answers=o['final_answers'],model=o['models'],effort=o['efforts'],requested_situation='Baywell pharmacy on Castro closing tonight, Monday12October2026,09:15SanFrancisco');Path('BLINDED').mkdir(exist_ok=True);(Path('BLINDED')/f'{rid}.json').write_text(json.dumps(b,indent=2)+'\n')
  (Path('runs')/rid/'TRANSCRIPT.md').write_text('# Intended initial prompt\n\n'+d['prompt']+'\n\n# Public observable events\n\n'+ '\n\n'.join(json.dumps(e,ensure_ascii=False,indent=2) for e in o['observable_events']))
completed=[x['run_id'] for x in s if (Path('runs')/x['run_id']/'completion.json').exists()];live=[];unstarted=[]
for x in s:
 r=x['run_id'];a=Path('runs')/r/'attempts/a1';h=a/'handle.json'
 if r in completed:continue
 if h.exists():live.append(dict(run_id=r,**json.loads(h.read_text())))
 else:unstarted.append(r)
Path('lanes/3/STATUS.json').write_text(json.dumps(dict(updated_utc=now(),completed_ids=completed,live_handles=live,unstarted_ids=unstarted,actual_terminal_errors=[],max_active=2),indent=2)+'\n')
