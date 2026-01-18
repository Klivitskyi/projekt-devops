"""
Testy jednostkowe dla aplikacji
"""
import pytest
from src.app import app


@pytest.fixture
def client():
    """Fixture tworzący klienta testowego"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test endpointu health check"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data


def test_info_endpoint(client):
    """Test endpointu info"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['application'] == 'DevOps Demo Application'
    assert 'version' in data


def test_echo_endpoint(client):
    """Test endpointu echo"""
    test_data = {'message': 'test', 'value': 123}
    response = client.post('/api/echo', json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'received' in data
    assert data['received'] == test_data


def test_metrics_endpoint(client):
    """Test endpointu metrics Prometheus"""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert response.content_type == 'text/plain; version=0.0.4; charset=utf-8'
    # Sprawdź czy zawiera podstawowe metryki
    metrics_text = response.get_data(as_text=True)
    assert 'http_requests_total' in metrics_text
    assert 'http_request_duration_seconds' in metrics_text
    assert 'http_requests_active' in metrics_text
    assert 'app_info' in metrics_text

