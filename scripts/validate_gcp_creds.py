import json
import os
import traceback

path = os.path.join(os.path.dirname(__file__), '..', 'google_service_account.json')
path = os.path.abspath(path)
print('Checking file:', path)

try:
    with open(path, 'r', encoding='utf-8-sig') as f:
        payload = json.load(f)
    print('Top-level keys:', list(payload.keys()))
except Exception as e:
    print('Failed reading JSON:', e)
    traceback.print_exc()
    raise SystemExit(1)

# Try to create service account credentials and refresh token
try:
    from google.oauth2.service_account import Credentials
    from google.auth.transport.requests import Request
except Exception as e:
    print('Missing google auth libs:', e)
    traceback.print_exc()
    raise SystemExit(1)

try:
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    creds = Credentials.from_service_account_file(path, scopes=scopes)
    print('Created Credentials object. client_email=', getattr(creds, 'service_account_email', None))
    print('Token URI:', creds.token_uri)
    print('Attempting to refresh credentials (network call)...')
    creds.refresh(Request())
    print('Refresh successful. Access token snippet:', creds.token[:20])
except Exception as e:
    print('Error during credential refresh:', type(e).__name__, str(e))
    traceback.print_exc()
    raise SystemExit(1)

print('Credentials validated successfully.')
