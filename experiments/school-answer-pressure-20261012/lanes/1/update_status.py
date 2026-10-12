import json
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2]
schedule=json.loads((root/'lanes/1/SCHEDULE.json').read_text())
complete=[];active=[];attempts={};errors=[];unstarted=[]
for d in schedule:
 r=d['run_id'];p=root/'runs'/r
 if (p/'completion.json').exists():complete.append(r)
 aps=sorted((p/'attempts').glob('a*')) if p.exists() else []
 attempts[r]=len(aps)
 if not aps:unstarted.append(r)
 for a in aps:
  if (a/'terminal.json').exists():
   t=json.loads((a/'terminal.json').read_text())
   if t['status']!='completed':errors.append(t)
  elif (a/'handle.json').exists():active.append({'run_id':r,'attempt':int(a.name[1:]),'handle':json.loads((a/'handle.json').read_text())['agent_path'],'stage':max(int(x.stem) for x in (a/'turns').glob('*.json'))})
status={'updated_utc':datetime.now(timezone.utc).isoformat(),'lane':1,'completed_ids':complete,'active':active,'attempts':attempts,'unstarted_ids':unstarted,'terminal_errors':errors,'max_parallelism':1 if errors else 2}
(root/'lanes/1/STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status))
