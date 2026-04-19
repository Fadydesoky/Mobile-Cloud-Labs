import unittest
from unittest.mock import MagicMock, patch

class TestLab2Backend(unittest.TestCase):

    @patch('redis.Redis')
    def test_redis_set_get(self, mock_redis):
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        mock_instance.get.return_value = b'value'

        client = mock_redis()
        client.set('key', 'value')

        result = client.get('key').decode('utf-8')
        self.assertEqual(result, 'value')

    @patch('redis.Redis')
    def test_non_existing_key(self, mock_redis):
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        mock_instance.get.return_value = None

        client = mock_redis()
        result = client.get('missing_key')

        self.assertIsNone(result)

    @patch('redis.Redis')
    def test_overwrite_value(self, mock_redis):
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        mock_instance.get.side_effect = [b'first', b'second']

        client = mock_redis()

        client.set('key', 'first')
        self.assertEqual(client.get('key').decode(), 'first')

        client.set('key', 'second')
        self.assertEqual(client.get('key').decode(), 'second')


if __name__ == '__main__':
    unittest.main()
