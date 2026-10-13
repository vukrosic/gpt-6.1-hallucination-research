"""Local fictional assistant tool service. No network or phone actions."""
import datetime
import fcntl
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
run_id, raw = sys.argv[1:3]
request = json.loads(raw)
path = root / 'mock_data' / (run_id + '.json')
with open(str(path) + '.lock', 'a') as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    state = json.loads(path.read_text())
    fixture = state['fixture']
    op = request.get('op')
    if op == 'help':
        result = {'operations': {
            'find_businesses': {'description': 'Find business listings.', 'arguments': {'query': 'string'}},
            'get_business_page': {'description': 'Retrieve a business page.', 'arguments': {'business_id': 'string'}},
            'place_call': {'description': 'Call a business with a message.', 'arguments': {'phone_number': 'string', 'message': 'string'}}}}
    elif op == 'find_businesses':
        result = fixture['find_businesses']
    elif op == 'get_business_page':
        result = fixture['get_business_page'] if request.get('business_id') == fixture['get_business_page']['business_id'] else {'error': 'business_not_found'}
    elif op == 'place_call':
        result = fixture['place_call'] if request.get('phone_number') == fixture['get_business_page']['phone'] else {'connected': False, 'detail': 'Number unavailable.'}
    else:
        result = {'error': 'unknown_operation'}
    state['log'].append({'seq': len(state['log']) + 1, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'request': request, 'response': result})
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))
