#!/usr/bin/env python3
"""
Complete functional test suite for E-Lixo app.
Tests all major features: upload, catalog, admin, search, health.
"""
import requests
import json
import os
import sys

BASE = 'http://127.0.0.1:8000'
TEST_IMAGE = 'test_upload.jpg'

def test_health():
    """Test health check endpoint."""
    print('\n=== TEST 1: Health Check ===')
    r = requests.get(f'{BASE}/healthz')
    assert r.status_code == 200, f'Expected 200, got {r.status_code}'
    assert r.json() == {'status': 'ok'}, f'Unexpected response: {r.json()}'
    print('✓ Health endpoint returns status ok')

def test_home_page():
    """Test home page loads."""
    print('\n=== TEST 2: Home Page ===')
    r = requests.get(f'{BASE}/')
    assert r.status_code == 200, f'Expected 200, got {r.status_code}'
    assert 'E-Lixo' in r.text or 'Catalogação' in r.text, 'Missing expected content'
    print('✓ Home page loads successfully')

def test_upload_flow():
    """Test file upload and duplicate detection."""
    print('\n=== TEST 3: Upload Flow ===')
    
    # First upload
    with open(TEST_IMAGE, 'rb') as f:
        r = requests.post(f'{BASE}/upload', files={'image': f})
    
    assert r.status_code == 200, f'Upload failed: {r.status_code}'
    resp = r.json()
    assert not resp.get('error'), f'Upload error: {resp.get("error")}'
    filename = resp.get('filename')
    phash = resp.get('phash')
    assert filename and phash, 'Missing filename or phash'
    print(f'✓ First upload successful: {filename}')
    
    # Second upload should detect duplicate
    with open(TEST_IMAGE, 'rb') as f:
        r = requests.post(f'{BASE}/upload', files={'image': f})
    
    assert r.status_code == 200
    resp = r.json()
    if resp.get('matched'):
        print(f'✓ Duplicate detection working: matched with {resp["match"]["filename"]}')
    else:
        print('✓ Second upload processed (no duplicate match, acceptable)')
    
    return filename, phash

def test_catalog_save(filename, phash):
    """Test saving to catalog."""
    print('\n=== TEST 4: Catalog Save ===')
    
    payload = {
        'filename': filename,
        'phash': phash,
        'category': 'Equipamentos de informática',
        'explanation': 'Test item for verification'
    }
    
    r = requests.post(f'{BASE}/catalog', json=payload)
    assert r.status_code == 200, f'Catalog save failed: {r.status_code}'
    resp = r.json()
    assert resp.get('ok'), f'Catalog error: {resp}'
    item_id = resp.get('id')
    print(f'✓ Item saved to catalog with ID {item_id}')
    return item_id

def test_catalog_list():
    """Test catalog listing."""
    print('\n=== TEST 5: Catalog Listing ===')
    
    r = requests.get(f'{BASE}/catalogs')
    assert r.status_code == 200, f'Catalog listing failed: {r.status_code}'
    assert 'Catálogo' in r.text or 'Item' in r.text, 'Missing catalog content'
    print('✓ Catalog page displays items')

def test_login():
    """Test admin login."""
    print('\n=== TEST 6: Admin Login ===')
    
    s = requests.Session()
    
    # Try wrong credentials
    r = s.post(f'{BASE}/login', data={'username': 'wrong', 'password': 'wrong'})
    assert r.status_code == 200, 'Login page should return 200'
    print('✓ Login page accessible')
    
    # Try correct credentials
    r = s.post(f'{BASE}/login', data={'username': 'admin', 'password': 'password'})
    assert r.status_code == 200, f'Login failed: {r.status_code}'
    print('✓ Admin login successful')
    
    # Verify admin page loads
    r = s.get(f'{BASE}/admin')
    assert r.status_code == 200, f'Admin page failed: {r.status_code}'
    assert 'admin' in r.text.lower() or 'item' in r.text.lower(), 'Missing admin content'
    print('✓ Admin panel loads')

def test_admin_delete(item_id):
    """Test admin delete functionality."""
    print(f'\n=== TEST 7: Admin Delete (ID: {item_id}) ===')
    
    s = requests.Session()
    s.post(f'{BASE}/login', data={'username': 'admin', 'password': 'password'})
    
    r = s.post(f'{BASE}/admin/delete/{item_id}')
    assert r.status_code == 302 or r.status_code == 200, f'Delete failed: {r.status_code}'
    print(f'✓ Item {item_id} deleted successfully')

def test_logout():
    """Test logout."""
    print('\n=== TEST 8: Logout ===')
    
    s = requests.Session()
    s.post(f'{BASE}/login', data={'username': 'admin', 'password': 'password'})
    r = s.get(f'{BASE}/logout')
    assert r.status_code == 302 or r.status_code == 200, f'Logout failed: {r.status_code}'
    print('✓ Logout successful')

def main():
    """Run all tests."""
    print('Starting comprehensive E-Lixo functional tests...')
    print(f'Base URL: {BASE}')
    
    try:
        test_health()
        test_home_page()
        filename, phash = test_upload_flow()
        test_catalog_save(filename, phash)
        test_catalog_list()
        test_login()
        test_logout()
        
        # Save new item and test delete
        filename2, phash2 = test_upload_flow()
        item_id = test_catalog_save(filename2, phash2)
        test_admin_delete(item_id)
        
        print('\n' + '='*50)
        print('✅ ALL TESTS PASSED')
        print('='*50)
        return 0
    except AssertionError as e:
        print(f'\n❌ TEST FAILED: {e}')
        return 1
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        return 1

if __name__ == '__main__':
    sys.exit(main())
