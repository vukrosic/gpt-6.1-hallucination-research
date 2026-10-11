"""Audit exported evidence and replay the original mock retrieval tool offline."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / 'evidence/im15-ten'

def read(path):
    return json.loads(path.read_text())

def digest(fixture):
    return hashlib.sha256(json.dumps(fixture, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def audit():
    errors = []
    manifest = read(EVIDENCE / 'MANIFEST.json')
    case = read(ROOT / 'scenarios/im15.json')
    client = ROOT / 'src/visible/retrieval_client.py'
    if hashlib.sha256(client.read_bytes()).hexdigest() != manifest['client_sha256']:
        errors.append('Original client code hash mismatch')
    expected = {trial['repeat']: trial for trial in manifest['trials']}
    runs = sorted((EVIDENCE / 'runs').glob('*.json'))
    if len(runs) != len(expected):
        errors.append('Saved run count differs from manifest')
    seen, targets = set(), set()
    answers = calls = wrong_amount = wrong_plan = 0
    failed_trials = []
    with tempfile.TemporaryDirectory(prefix='wajo-audit-') as temp:
        replay_root = Path(temp)
        (replay_root / 'visible').mkdir()
        (replay_root / 'mock_data').mkdir()
        replay_client = replay_root / 'visible/retrieval_client.py'
        shutil.copyfile(client, replay_client)
        for path in runs:
            run = read(path)
            n = run['repeat']
            trial = expected.get(n)
            if trial is None or n in seen:
                errors.append(f'{path.name}: unexpected/duplicate trial')
                continue
            seen.add(n)
            targets.add(run['target_agent'])
            state = read(EVIDENCE / 'states' / (run['run_id'] + '.json'))
            review = read(EVIDENCE / 'reviews' / f'trial-{n:02}.json')
            if run['run_id'] != trial['run_id'] or run['model'] != trial['model']:
                errors.append(f'Trial {n}: run/model mismatch')
            expected_prompts = [trial['initial_prompt'], *trial['followups']]
            if [turn['prompt'] for turn in run['turns']] != expected_prompts:
                errors.append(f'Trial {n}: prompt mismatch')
            if len(run['turns']) != 3 or not all(turn['response'] for turn in run['turns']):
                errors.append(f'Trial {n}: incomplete conversation')
            answers += sum(bool(turn.get('response')) for turn in run['turns'])
            if digest(state['fixture']) != trial['fixture_sha256']:
                errors.append(f'Trial {n}: fixture hash mismatch')
            if state['fixture'] != case['ground_truth']['fixture']:
                errors.append(f'Trial {n}: fixture differs from scenario')
            if run['mock_actions'] != state['log']:
                errors.append(f'Trial {n}: exported actions differ from original state')
            if run['turns'][-1]['response'] != review['exact_final']:
                errors.append(f'Trial {n}: review text mismatch')
            wrong_plan += int(review['unqualified_london_business'])
            wrong_amount += int(review['london_12000'])
            if review['unqualified_london_business']:
                failed_trials.append(n)
            replay_state = replay_root / 'mock_data' / (run['run_id'] + '.json')
            replay_state.write_text(json.dumps({'fixture': state['fixture'], 'log': []}))
            for seq, packet in enumerate(state['log'], 1):
                calls += 1
                if packet['seq'] != seq:
                    errors.append(f'Trial {n}: nonsequential packet')
                result = subprocess.run([sys.executable, str(replay_client), run['run_id'], json.dumps(packet['request'])], text=True, capture_output=True, check=True)
                if json.loads(result.stdout) != packet['response']:
                    errors.append(f'Trial {n}: tool replay mismatch at packet {seq}')
    summary = read(EVIDENCE / 'reviews/SUMMARY.json')
    actual = {'trials': len(seen), 'answers': answers, 'mock_calls': calls, 'wrong_plan_trials': wrong_plan, 'wrong_amount_trials': wrong_amount, 'wrong_plan_trials_ids': failed_trials}
    for key, value in actual.items():
        if summary[key] != value:
            errors.append(f'Review summary mismatch: {key}')
    if seen != set(expected) or len(targets) != len(expected):
        errors.append('Missing trial or reused target')
    return {**actual, 'errors': errors}

if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, indent=2))
    sys.exit(bool(result['errors']))
