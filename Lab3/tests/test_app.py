import unittest
from Lab3.app import app


class TestLabThreeAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health(self):
        res = self.client.get('/health')
        self.assertEqual(res.status_code, 200)

    def test_home(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        self.assertIn('message', data)

    def test_data_default(self):
        res = self.client.get('/data')
        self.assertEqual(res.status_code, 200)

    def test_data_custom(self):
        res = self.client.get('/data?size=50')
        self.assertIn(res.status_code, [200, 400])

    def test_invalid_endpoint(self):
        res = self.client.get('/wrong')
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
