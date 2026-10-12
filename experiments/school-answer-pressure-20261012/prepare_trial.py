"""Print the three prompts for a fresh local reproduction; never calls a model."""
from pathlib import Path
import json,re,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parent

def prepare(run_id,condition):
    if condition not in ('neutral','pressure'):raise ValueError('Use neutral or pressure')
    if not re.fullmatch(r'[A-Za-z0-9_-]+',run_id):raise ValueError('Use an opaque alphanumeric run ID')
    protocol=json.loads((ROOT/'PROTOCOL.json').read_text())
    runtime=Path(tempfile.mkdtemp(prefix='records_'))
    shutil.copyfile(ROOT/'client.py',runtime/'client.py')
    (runtime/'cases'/protocol['case']).mkdir(parents=True)
    shutil.copyfile(ROOT/'SOURCE.json',runtime/'cases'/protocol['case']/'source.json')
    (runtime/'runs'/run_id).mkdir(parents=True)
    first=protocol['initial_prompt_template'].replace(protocol['runtime_root'],str(runtime)).replace('OPAQUE_RUN',run_id)
    return {'model':'gpt-6.1-sol','reasoning_effort':'low','fork_turns':'none','prompts':[first,protocol['turn2'],protocol['turn3'][condition]],'runtime_root':str(runtime),'instructions':'Send only prompt 1 to a fresh native agent. After it completes, send prompt 2 to the SAME agent. After that completes, send prompt 3. Keep the study condition, grading rubric and other traces out of the target conversation.'}
if __name__=='__main__':print(json.dumps(prepare(*sys.argv[1:]),ensure_ascii=False,indent=2))
