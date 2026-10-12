"""Read one native target's observable task trace, excluding private context."""
from pathlib import Path
import json
import sys


def capture(agent_path):
    directory = Path('/Users/vukrosic/.codex/sessions/2026/10')
    candidates = []
    for path in list(directory.glob('11/*.jsonl')) + list(directory.glob('12/*.jsonl')):
        with path.open() as stream:
            first_line = stream.readline()
            if not first_line.strip():
                continue
            first = json.loads(first_line)
        meta = first.get('payload', {})
        if first.get('type') == 'session_meta' and meta.get('agent_path') == agent_path:
            candidates.append((path, meta))
    if len(candidates) != 1:
        raise ValueError(f'Expected one native session for {agent_path}; found {len(candidates)}')
    path, meta = candidates[0]
    models, efforts, events, finals = set(), set(), [], []
    for line in path.read_text().splitlines():
        row = json.loads(line)
        payload = row.get('payload', {})
        if row.get('type') == 'turn_context':
            models.add(payload.get('model'))
            efforts.add(payload.get('effort'))
        if row.get('type') != 'response_item':
            continue
        kind = payload.get('type')
        if kind in ['function_call', 'function_call_output', 'custom_tool_call', 'custom_tool_call_output']:
            events.append({'utc': row.get('timestamp'), **{k: payload[k] for k in ['type', 'name', 'call_id', 'input', 'arguments', 'output', 'status'] if k in payload}})
        elif kind == 'message' and payload.get('role') == 'assistant':
            phase = payload.get('phase')
            channel = payload.get('channel')
            if phase == 'final_answer':
                channel = 'final'
            elif phase == 'commentary':
                channel = 'commentary'
            elif phase is not None or channel not in [None, 'final', 'commentary']:
                continue
            text = ''.join(block.get('text', '') for block in payload.get('content', []) if block.get('type') == 'output_text')
            channel = channel or 'final'
            events.append({'utc': row.get('timestamp'), 'type': 'assistant_message', 'channel': channel, 'text': text})
            if channel == 'final':
                finals.append(text)
    return {'agent_path': agent_path, 'native_session_id': meta.get('id'), 'models': sorted(models), 'efforts': sorted(efforts, key=str), 'observable_events': events, 'final_answers': finals, 'prompt_provenance': 'Use separately preserved exact coordinator dispatch text. Native incoming context is excluded.', 'excluded': ['Private internal reasoning', 'Encrypted reasoning', 'System and developer instructions', 'Other native context']}


if __name__ == '__main__':
    result = capture(sys.argv[1])
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(serialized)
        print(f'Saved observable trace for {result["agent_path"]}; {len(result["final_answers"])} final answer(s).')
    else:
        print(serialized)
