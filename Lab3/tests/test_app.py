import unittest
import json
from Lab3.app import app


class TestLabThreeAPI(unittest.TestCase):
    """Comprehensive test suite for Lab3 API endpoints"""

    def setUp(self):
        """Initialize test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_health_endpoint_success(self):
        """Test health check endpoint returns 200 OK"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'ok')

    def test_home_endpoint_returns_json(self):
        """Test home endpoint returns valid JSON with required fields"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('delay', data)
        self.assertEqual(data['message'], 'Mobile Cloud API')

    def test_home_endpoint_delay_in_range(self):
        """Test home endpoint delay is within expected range"""
        response = self.client.get('/')
        data = json.loads(response.data)
        delay = data['delay']
        self.assertGreaterEqual(delay, 0.1)
        self.assertLessEqual(delay, 1.5)

    def test_data_endpoint_default_size(self):
        """Test data endpoint with default size parameter"""
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('count', data)
        self.assertIn('sample', data)
        self.assertEqual(data['count'], 100)  # Default size
        self.assertEqual(len(data['sample']), 5)

    def test_data_endpoint_custom_size(self):
        """Test data endpoint with custom size parameter"""
        response = self.client.get('/data?size=50')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 50)

    def test_data_endpoint_max_size_limit(self):
        """Test data endpoint respects maximum size limit"""
        response = self.client.get('/data?size=10000')
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertIn('error', error_data)

    def test_data_endpoint_invalid_size_string(self):
        """Test data endpoint rejects invalid (non-integer) size"""
        response = self.client.get('/data?size=invalid')
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertIn('error', error_data)

    def test_data_endpoint_negative_size(self):
        """Test data endpoint rejects negative size"""
        response = self.client.get('/data?size=-10')
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertIn('error', error_data)

    def test_data_endpoint_zero_size(self):
        """Test data endpoint handles zero size"""
        response = self.client.get('/data?size=0')
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertIn('error', error_data)

    def test_nonexistent_endpoint(self):
        """Test 404 error for nonexistent endpoint"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_response_content_type(self):
        """Test API returns JSON content type"""
        response = self.client.get('/health')
        # Health endpoint returns plain text
        self.assertIn('text/plain', response.content_type)
        
    def test_home_response_content_type(self):
        """Test home endpoint returns JSON content type"""
        response = self.client.get('/')
        self.assertIn('application/json', response.content_type)

    def test_data_response_content_type(self):
        """Test data endpoint returns JSON content type"""
        response = self.client.get('/data')
        self.assertIn('application/json', response.content_type)

    def test_concurrent_requests_independence(self):
        """Test that multiple requests don't interfere with each other"""
        responses = [self.client.get('/') for _ in range(5)]
        self.assertEqual(len(responses), 5)
        for response in responses:
            self.assertEqual(response.status_code, 200)


class TestAPIErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_large_valid_size(self):
        """Test with maximum allowed size"""
        response = self.client.get('/data?size=5000')
        self.assertEqual(response.status_code, 200)

    def test_boundary_size_values(self):
        """Test boundary size values"""
        # Minimum valid
        response = self.client.get('/data?size=1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1)


if __name__ == '__main__':
    unittest.main()
