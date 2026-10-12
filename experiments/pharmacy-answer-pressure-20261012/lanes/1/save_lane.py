from pathlib import Path
import json,sys,datetime,hashlib
sys.path.insert(0,str(Path.cwd()))
from capture_observable import capture
base=Path.cwd(); lane=base/'lanes/1';s=json.loads((lane/'SCHEDULE.json').read_text());now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for rid in sys.argv[1:]:
 x=next(x for x in s if x['run_id']==rid);attempt_dirs=sorted((base/'runs'/rid/'attempts').glob('a*'));a=attempt_dirs[-1];d=json.loads((a/'dispatch-actual.json').read_text());ap=d.get('actual_path','/root/assistant_batch1/'+rid+'_'+a.name);o=capture(ap)
 if not o['final_answers']:continue
 (a/'observable.json').write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
 raw=json.loads(Path(x['runtime_root'],'mock_data',d.get('runtime_locator',rid)+'.json').read_text());logs=raw.get('log',[])
 (a/'client_calls.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in logs))
 d=json.loads((a/'dispatch-actual.json').read_text());lat=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(d['dispatch_utc'])).total_seconds()
 c=dict(logical_run_id=rid,attempt=int(a.name[1:]),status='completed',actual_path=ap,model=o['models'],effort=o['efforts'],completed_utc=now(),latency_seconds=lat,fixture_sha256=hashlib.sha256(json.dumps(raw['fixture'],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),source_sha256=x['source_sha256'],empty_reply=not any(o['final_answers']),prompt_provenance='Exact intended plaintext dispatch saved; native incoming context excluded and not independently plaintext verified.')
 (a/'completion.json').write_text(json.dumps(c,indent=2)+'\n')
 for f in ['observable.json','client_calls.jsonl']:(base/'runs'/rid/f).write_bytes((a/f).read_bytes())
 (base/'runs'/rid/'completion.json').write_text(json.dumps(dict(c,successful_attempt='attempts/'+a.name),indent=2)+'\n')
 bp=base/'BLINDED';bp.mkdir(exist_ok=True)
 (bp/(rid+'.json')).write_text(json.dumps(dict(logical_run_id=rid,source_fixture=raw['fixture'],source_sha256=x['source_sha256'],actual_final_answers=o['final_answers'],model=o['models'],effort=o['efforts'],requested_situation='Baywell pharmacy on Castro closing tonight, Monday12October2026,09:15SanFrancisco'),indent=2,ensure_ascii=False)+'\n')
 tr='# '+rid+'\n\n## Exact intended initial prompt\n\n'+x['prompt']+'\n\n## Public observable events\n\n'+''.join('```json\n'+json.dumps(v,indent=2,ensure_ascii=False)+'\n```\n\n' for v in o['observable_events'])
 (base/'runs'/rid/'TRANSCRIPT.md').write_text(tr)
 print(rid,'saved',len(logs),'client logs')
complete=[x['run_id'] for x in s if (base/'runs'/x['run_id']/'completion.json').exists()];dispatched=[x['run_id'] for x in s if (base/'runs'/x['run_id']/'attempts/a1/dispatch-actual.json').exists()];live=[];errors=[];attempts={}
for r in dispatched:
 ads=sorted((base/'runs'/r/'attempts').glob('a*'));attempts[r]=[a.name for a in ads]
 for a in ads:
  if (a/'terminal.json').exists():errors.append(dict(run_id=r,attempt=a.name,**json.loads((a/'terminal.json').read_text())))
  elif not (a/'completion.json').exists():
   d=json.loads((a/'dispatch-actual.json').read_text());live.append(dict(run_id=r,actual_path=d.get('actual_path','/root/assistant_batch1/'+r+'_'+a.name)))
(lane/'STATUS.json').write_text(json.dumps(dict(updated_utc=now(),max_active=1 if errors else 2,completed_ids=complete,live_handles=live,attempts=attempts,unstarted_ids=[x['run_id'] for x in s if x['run_id'] not in dispatched],actual_terminal_errors=errors),indent=2)+'\n')
