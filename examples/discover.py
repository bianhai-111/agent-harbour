"""Public MCP discovery and draft only; never creates an account or task."""
import json
import urllib.request

URL = 'https://kicorn.com/api/mcp'

def rpc(method, params):
    request = urllib.request.Request(
        URL,
        data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode(),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'User-Agent': 'Agent-Harbour-Public-Example/1.0'},
        method='POST',
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if 'error' in result:
        raise RuntimeError(result['error']['message'])
    return result['result']

if __name__ == '__main__':
    print(rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'public example', 'version': '1.0'}})['serverInfo'])
    print('Tools:', [tool['name'] for tool in rpc('tools/list', {})['tools']])
    draft = rpc('tools/call', {'name': 'prepare_task', 'arguments': {
        'task_type': 'CUSTOM', 'category': 'DIGITAL',
        'question': 'Write a short product introduction using my supplied notes; do not invent features.',
        'location': 'Online', 'currency': 'USD', 'amount': 0, 'language': 'en',
    }})
    if draft.get('isError'):
        raise RuntimeError(draft['content'][0]['text'])
    print(json.dumps(draft.get('structuredContent'), indent=2, ensure_ascii=False))
