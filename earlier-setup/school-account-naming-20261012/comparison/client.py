from pathlib import Path
from datetime import datetime,timezone
import json,sys
b=Path(__file__).resolve().parent
case,run=sys.argv[1:3]
req=json.loads(sys.argv[3]); records=json.loads((b/'cases'/case/'source.json').read_text())['records'];op=req.get('op')
if op=='help': result={'operations':{'records':'List record ids and titles','read':'Read document id','search':'Search titles and text by query'}}
elif op=='records':result=[{'id':k,'title':v['title']} for k,v in records.items()]
elif op=='read':result=records.get(req.get('id'),{'error':'Unknown document'})
elif op=='search':result=[{'id':k,'title':v['title'],'snippet':v['text'][:150]} for k,v in records.items() if req.get('query','').lower() in (v['title']+' '+v['text']).lower()]
else:result={'error':'Unknown operation'}
with (b/'runs'/run/'client_calls.jsonl').open('a') as f:f.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'request':req,'response':result})+'\n')
print(json.dumps(result))
