import unittest
from flask import json
from your_flask_app import create_app

class Lab3TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_get_endpoint(self):
        response = self.client.get('/your_get_endpoint')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

    def test_post_endpoint_valid(self):
        response = self.client.post('/your_post_endpoint', 
                                      data=json.dumps({'key': 'value'}), 
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_post_endpoint_invalid(self):
        response = self.client.post('/your_post_endpoint', 
                                      data=json.dumps({'invalid_key': 'value'}), 
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_error_handling(self):
        response = self.client.get('/non_existing_endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    def test_input_validation(self):
        response = self.client.post('/your_post_endpoint', 
                                      data=json.dumps({'key': None}), 
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
