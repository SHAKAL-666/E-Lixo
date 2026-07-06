import os
import tempfile
import unittest
from unittest import mock

from app import classify_with_vision_api


class VisionCredentialsTests(unittest.TestCase):
    def test_malformed_service_account_returns_error_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            invalid_path = os.path.join(tmpdir, 'service-account.json')
            with open(invalid_path, 'w', encoding='utf-8') as f:
                f.write('{"type": "service_account", "project_id": "dummy"}')

            with mock.patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': invalid_path}, clear=False):
                result = classify_with_vision_api('dummy-image.jpg')

        self.assertIsNotNone(result)
        self.assertEqual(result['error'], 'invalid_credentials')
        self.assertIn('credencial', result['message'].lower())


if __name__ == '__main__':
    unittest.main()
