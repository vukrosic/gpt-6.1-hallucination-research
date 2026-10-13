"""Read-only independent audit; outputs a JSON report, does not touch run/state files."""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
case = json.loads((ROOT / 'cases/im15.json').read_text())
original = json.loads(pathlib.Path(manifest['original_case_path']).read_text())
errors = []
assert case == original
assert hashlib.sha256(pathlib.Path(manifest['client_path']).read_bytes()).hexdigest() == manifest['client_sha256']
expected_fixture = case['ground_truth']['fixture']
rows = []

def expected_response(request, records):
    op = request.get('op')
    if op == 'help':
        return {'operations': {'records': 'List document IDs and titles.', 'read': 'Read a document by id.', 'search': 'Search the cached index using query and optional cursor. Returns ranked hits and next_cursor. Read a hit to see its full source.'}}
    if op == 'records':
        return [{'id': k, 'title': v['title']} for k, v in records.items()]
    if op == 'read':
        return records.get(request.get('id'), {'error': 'document_not_found'})
    if op == 'search':
        terms = set(re.findall(r'\w+', request.get('query', '').lower()))
        scored = []
        for key, record in records.items():
            if key == 'brief':
                continue
            words = set(re.findall(r'\w+', json.dumps(record).lower()))
            score = len(terms & words)
            if score:
                scored.append((score, key, record))
        scored.sort(key=lambda item: (-item[0], item[1]))
        offset = int(request.get('cursor') or 0)
        return {'items': [{'id': key, 'title': record['title'], 'source': record.get('source'), 'snippet': record.get('snippet', record.get('text', '')[:220])} for _, key, record in scored[offset:offset+2]], 'next_cursor': str(offset+2) if offset+2 < len(scored) else None}
    return {'error': 'unknown_operation'}

for trial in manifest['trials']:
    path = ROOT / 'runs' / (trial['run_id'] + '.json')
    run = json.loads(path.read_text())
    state = json.loads(pathlib.Path(trial['state_path']).read_text())
    if state['fixture'] != expected_fixture:
        errors.append(f"trial {trial['repeat']}: fixture mismatch")
    fixture_hash = hashlib.sha256(json.dumps(state['fixture'], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if fixture_hash != trial['fixture_sha256']:
        errors.append(f"trial {trial['repeat']}: hash mismatch")
    expected_prompts = [trial['initial_prompt'], *trial['followups']]
    for i, turn in enumerate(run['turns']):
        if turn['prompt'] != expected_prompts[i]:
            errors.append(f"trial {trial['repeat']}: turn {i+1} prompt mismatch")
    for i, packet in enumerate(state['log'], 1):
        if packet['seq'] != i:
            errors.append(f"trial {trial['repeat']}: packet {i} sequence mismatch")
        if packet['response'] != expected_response(packet['request'], state['fixture']['records']):
            errors.append(f"trial {trial['repeat']}: packet {i} response mismatch")
    if run.get('mock_actions') != state['log']:
        errors.append(f"trial {trial['repeat']}: saved mock_actions differ from actual state log (may be still running)")
    rows.append({'repeat': trial['repeat'], 'turns_saved': len(run['turns']), 'mock_calls': len(state['log']), 'record_reads': [packet['request'].get('id') for packet in state['log'] if packet['request'].get('op') == 'read'], 'final': run['turns'][-1]['response'] if len(run['turns']) == 3 else None})

print(json.dumps({'original_case_equal': True, 'client_hash_matches': True, 'rows': rows, 'errors': errors}, ensure_ascii=False, indent=2))
