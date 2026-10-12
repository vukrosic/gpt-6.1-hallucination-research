"""Prepare or preserve actual native conversations. Does not run models or grade answers."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,sys
from capture_observable import capture
ROOT=Path(__file__).resolve().parent
now=lambda:datetime.now(timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text())
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
    mode,rid,n,*args=sys.argv[1:];n=int(n)
    d=next(d for d in read(ROOT/'SCHEDULE.json') if d['run_id']==rid)
    protocol=read(ROOT/'PROTOCOL.json');runtime=Path(protocol['runtime_root'])
    trial=ROOT/'runs'/rid;ap=trial/'attempts'/f'a{n}'
    locator=f'{rid}_a{n}'
    if mode=='prepare':
        assert not (trial/'completion.json').exists(),'Never rerun completed reply'
        assert not ap.exists(),'Already prepared: inspect actual handle before any dispatch'
        ap.mkdir(parents=True);write(runtime/'mock_data'/f'{locator}.json',{'fixture':read(ROOT/'SOURCE.json'),'log':[]})
        prompt=protocol['initial_prompt_template'].replace('OPAQUE_RUN',locator)
        actual={'logical_run_id':rid,'attempt':n,'locator':locator,'dispatch_utc':now(),'prompt':prompt,'followups':d['followups'],'model':d['model'],'effort':d['effort'],'fork_turns':d['fork_turns']}
        write(ap/'dispatch-actual.json',actual)
        write(ap/'turns/1.json',{'turn':1,'dispatch_utc':actual['dispatch_utc'],'prompt':prompt})
        print(json.dumps(actual,ensure_ascii=False))
        return
    if mode=='handle':
        write(ap/'handle.json',{'agent_path':args[0],'attached_utc':now()});return
    if mode=='turn':
        turn=int(args[0]);assert turn in [2,3]
        assert not (ap/f'turns/{turn}.json').exists(),'Followup already recorded; do not duplicate'
        value={'turn':turn,'dispatch_utc':now(),'prompt':d['followups'][turn-2]}
        write(ap/f'turns/{turn}.json',value);print(json.dumps(value,ensure_ascii=False));return
    if mode not in ['finish','failed']:raise ValueError(mode)
    path=read(ap/'handle.json')['agent_path']
    observable=capture(path);write(ap/'observable.json',observable)
    state=read(runtime/'mock_data'/f'{locator}.json')
    (ap/'client_calls.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in state['log']))
    dispatch=read(ap/'dispatch-actual.json')
    if mode=='finish':
        assert len(observable['final_answers'])==3,('Expected three actual final answers',observable['final_answers'])
        assert all((ap/f'turns/{i}.json').exists() for i in [1,2,3])
        assert observable['models']==['gpt-6.1-sol'] and observable['efforts']==['low']
    terminal={'logical_run_id':rid,'attempt':n,'agent_path':path,'status':'completed' if mode=='finish' else 'capacity_failed',
              'completed_utc':now(),'latency_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(dispatch['dispatch_utc'])).total_seconds(),
              'actual_final_answer_count':len(observable['final_answers']),'incoming_plaintext_verified':False,'actual_error':args[0] if args else None}
    write(ap/'terminal.json',terminal)
    if mode=='failed':return
    assert not (trial/'completion.json').exists(),'Already completed'
    for name in ['observable.json','client_calls.jsonl']:shutil.copyfile(ap/name,trial/name)
    write(trial/'completion.json',terminal)
    packet={'logical_run_id':rid,'source_fixture':read(ROOT/'SOURCE.json'),'source_sha256':d['source_sha256'],
            'actual_final_answer':observable['final_answers'][-1],'requested_situation':read(ROOT/'GRADING.json')['requested_situation'],
            'models':observable['models'],'efforts':observable['efforts']}
    target=ROOT/'BLINDED'/f'{rid}.json';assert not target.exists();write(target,packet)
    events=[{'utc':read(ap/f'turns/{i}.json')['dispatch_utc'],'type':'intended_user_prompt','turn':i,'text':read(ap/f'turns/{i}.json')['prompt']} for i in [1,2,3]]+observable['observable_events']
    events.sort(key=lambda e:e.get('utc') or '')
    text='# Full public conversation '+rid+'\n\nExact intended prompts and actual public tool calls/results and replies, in timestamp order. Private internal reasoning is excluded.\n\n'
    for e in events:
        text+='## '+str(e.get('utc',''))+' — '+e['type']+'\n\n'
        if e['type'] in ['intended_user_prompt','assistant_message']:
            text+='```text\n'+e['text']+'\n```\n\n'
        else:text+='```json\n'+json.dumps(e,ensure_ascii=False,indent=2)+'\n```\n\n'
    (trial/'TRANSCRIPT.md').write_text(text)
    print(f'Saved {rid}: all three turns, actual calls, and blinded final reply.')
if __name__=='__main__':main()
