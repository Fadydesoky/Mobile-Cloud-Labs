import unittest
from unittest.mock import patch
from Lab2.app import app


class TestRedisAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('Lab2.app.redis_primary')
    def test_write_success(self, mock_redis):
        mock_redis.set.return_value = True

        response = self.client.get('/write')
        self.assertEqual(response.status_code, 200)

    def test_write_no_redis(self):
        with patch('Lab2.app.redis_primary', None):
            response = self.client.get('/write')
            self.assertEqual(response.status_code, 200)

    @patch('Lab2.app.redis_primary')
    def test_read_primary(self, mock_redis):
        mock_redis.get.return_value = 'hello'

        response = self.client.get('/read-primary')
        self.assertEqual(response.status_code, 200)

    @patch('Lab2.app.redis_replica')
    def test_read_replica(self, mock_redis):
        mock_redis.get.return_value = 'hello'

        response = self.client.get('/read-replica')
        self.assertEqual(response.status_code, 200)

    def test_endpoints_exist(self):
        endpoints = ['/', '/write', '/read-primary', '/read-replica']

        for ep in endpoints:
            response = self.client.get(ep)
            self.assertNotEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
