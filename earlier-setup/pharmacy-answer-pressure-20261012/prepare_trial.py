"""Prepare a fresh local mock client and exact prompt; never calls a model."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent

def prepare(run_id, arm):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', run_id):
        raise ValueError('Use an opaque run ID containing letters, digits, underscore or hyphen.')
    protocol = json.loads((ROOT/'PROTOCOL.json').read_text())
    runtime = Path(tempfile.mkdtemp(prefix='assistant_'))
    (runtime/'visible').mkdir()
    (runtime/'mock_data').mkdir()
    client = runtime/'visible/client.py'
    shutil.copyfile(ROOT/'client.py', client)
    fixture = json.loads((ROOT/'FIXTURE.json').read_text())
    state = runtime/'mock_data'/f'{run_id}.json'
    state.write_text(json.dumps({'fixture':fixture,'log':[]},ensure_ascii=False,indent=2)+'\n')
    old_client = str(Path(protocol['runtime_root'])/'visible/client.py')
    prompt = protocol['templates'][arm].replace(old_client,str(client)).replace('OPAQUE_RUN',run_id)
    return {'prompt':prompt,'model':'gpt-6.1-sol','reasoning_effort':'low','fork_turns':'none',
            'mock_state':str(state),'client':str(client),
            'fixture_sha256':hashlib.sha256((ROOT/'FIXTURE.json').read_bytes()).hexdigest(),
            'client_sha256':hashlib.sha256(client.read_bytes()).hexdigest()}

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_id')
    parser.add_argument('arm',choices=['strict','neutral'])
    args = parser.parse_args()
    print(json.dumps(prepare(args.run_id,args.arm),ensure_ascii=False,indent=2))
