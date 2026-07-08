import json
from pathlib import Path

paths = [Path.cwd() / 'google_service_account.json', Path('C:/Users/Dev2/Desktop/E-Lixo/google_service_account.json'), Path('C:/Users/Dev2/Desktop/e-lixo/google_service_account.json')]
for p in paths:
    print('PATH:', p)
    print('exists:', p.exists())
    if p.exists():
        print('size:', p.stat().st_size)
        text = p.read_text('utf-8-sig')
        print('head:', repr(text[:200]))
        print('--- lines ---')
        for i, line in enumerate(text.splitlines()[:20], 1):
            print(f'{i}: {line}')
        try:
            data = json.loads(text)
            print('keys:', list(data.keys()))
            print('token_uri present:', 'token_uri' in data)
        except Exception as e:
            print('json error:', type(e).__name__, e)
    print('---')
