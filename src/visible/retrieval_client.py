"""Local fictional retrieval service."""
import json, pathlib, sys, re, fcntl, datetime
ROOT=pathlib.Path(__file__).resolve().parent.parent
run_id,raw=sys.argv[1:3]
request=json.loads(raw)
path=ROOT/'mock_data'/(run_id+'.json')
lock=open(str(path)+'.lock','a');fcntl.flock(lock,fcntl.LOCK_EX)
state=json.loads(path.read_text());records=state['fixture']['records']
op=request.get('op')
if op=='help':
 result={'operations':{'records':'List document IDs and titles.','read':'Read a document by id.','search':'Search the cached index using query and optional cursor. Returns ranked hits and next_cursor. Read a hit to see its full source.'}}
elif op=='records':
 result=[{'id':k,'title':v['title']} for k,v in records.items()]
elif op=='read':
 result=records.get(request.get('id'),{'error':'document_not_found'})
elif op=='search':
 terms=set(re.findall(r'\w+',request.get('query','').lower()))
 scored=[]
 for k,v in records.items():
  if k=='brief':continue
  words=set(re.findall(r'\w+',json.dumps(v).lower()))
  score=len(terms&words)
  if score:scored.append((score,k,v))
 scored.sort(key=lambda x:(-x[0],x[1]));offset=int(request.get('cursor') or 0)
 selected=scored[offset:offset+2]
 result={'items':[{'id':k,'title':v['title'],'source':v.get('source'),'snippet':v.get('snippet',v.get('text','')[:220])} for score,k,v in selected],'next_cursor':str(offset+2) if offset+2<len(scored) else None}
else:result={'error':'unknown_operation'}
state['log'].append({'seq':len(state['log'])+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request':request,'response':result})
path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
