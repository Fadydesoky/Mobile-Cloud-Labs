"""
Unit tests for Order Service
"""
import pytest
import sys
import os
from unittest.mock import patch, Mock

# Add the parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'order-service'))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestOrderServiceHealth:
    """Tests for health and readiness endpoints"""

    def test_health_endpoint(self, client):
        """Test health endpoint returns correct status"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'order-service'
        assert data['status'] == 'up'
        assert 'time' in data
        assert 'version' in data

    @patch('app.requests.get')
    def test_ready_endpoint_with_product_service_up(self, mock_get, client):
        """Test readiness when product service is available"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = client.get('/ready')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ready'

    @patch('app.requests.get')
    def test_ready_endpoint_with_product_service_down(self, mock_get, client):
        """Test readiness when product service is unavailable"""
        mock_get.side_effect = Exception("Connection refused")

        response = client.get('/ready')
        assert response.status_code == 503
        data = response.get_json()
        assert data['status'] == 'not ready'


class TestOrderServiceOrders:
    """Tests for order creation endpoint"""

    @patch('app.fetch_product')
    def test_create_order_success(self, mock_fetch, client):
        """Test successful order creation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "name": "Laptop",
            "price": 1200
        }
        mock_fetch.return_value = (mock_response, 0.05)

        response = client.post('/orders',
            json={"product_id": 1, "quantity": 2},
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Order created'
        assert data['product'] == 'Laptop'
        assert data['quantity'] == 2
        assert data['total_price'] == 2400

    @patch('app.fetch_product')
    def test_create_order_product_not_found(self, mock_fetch, client):
        """Test order creation with invalid product"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_fetch.return_value = (mock_response, 0.05)

        response = client.post('/orders',
            json={"product_id": 999, "quantity": 1},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @patch('app.fetch_product')
    def test_create_order_service_unavailable(self, mock_fetch, client):
        """Test order creation when product service is down"""
        mock_fetch.return_value = (None, None)

        response = client.post('/orders',
            json={"product_id": 1, "quantity": 1},
            content_type='application/json'
        )
        assert response.status_code == 503
        data = response.get_json()
        assert 'error' in data
        assert data['resilience'] == 'retry exhausted'


class TestOrderServiceMetrics:
    """Tests for metrics endpoint"""

    def test_metrics_endpoint(self, client):
        """Test Prometheus metrics endpoint"""
        response = client.get('/metrics')
        assert response.status_code == 200
        assert b'order_service_requests_total' in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
