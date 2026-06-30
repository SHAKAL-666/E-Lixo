import unittest
import requests


class HealthEndpointTests(unittest.TestCase):
    def test_health_endpoint_returns_ok(self):
        response = requests.get('http://127.0.0.1:8000/healthz', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})


if __name__ == '__main__':
    unittest.main()
