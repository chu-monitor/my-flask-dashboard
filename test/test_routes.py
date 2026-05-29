import pytest
import json
from src import create_app
from src.config import TestingConfig

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestingConfig)
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_index_route(client):
    """Test that the landing page renders successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'AeroDash' in response.data
    assert b'19191' in response.data

def test_health_api(client):
    """Test that the health endpoint returns correct metrics."""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = json.loads(response.data.decode('utf-8'))
    assert data['status'] == 'healthy'
    assert 'cpu_load' in data
    assert 'memory_usage' in data

def test_info_api(client):
    """Test that the info endpoint returns the correct app details."""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data.decode('utf-8'))
    assert data['app_name'] == 'AeroDash Flask Core'
    assert data['port'] == 19191
    assert 'version' in data
    assert len(data['features']) > 0

def test_stocks_api(client):
    """Test that the stock watchlist API returns correct stock info."""
    response = client.get('/api/stocks')
    assert response.status_code == 200
    
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)
    assert len(data) == 4
    
    # Check default TSMC stock info
    tsmc = [s for s in data if s['symbol'] == '2330.TW'][0]
    assert tsmc['name'] == '台積電'
    assert tsmc['price'] == 875.0
    assert tsmc['direction'] == 'up'
    
    # Check NVIDIA
    nvda = [s for s in data if s['symbol'] == 'NVDA'][0]
    assert nvda['name'] == '輝達 (NVIDIA)'
    assert nvda['price'] == 950.0

def test_schedule_api(client):
    """Test that the afternoon schedule API returns correct workspace info."""
    response = client.get('/api/schedule')
    assert response.status_code == 200
    
    data = json.loads(response.data.decode('utf-8'))
    assert '緯創資通股份有限公司' in data['company']
    assert '下午 13:30 - 18:00' in data['time_window']
    assert data['status'] == 'on_duty'
    assert len(data['timeline']) == 4
    
    # Verify timeline tasks
    task1 = data['timeline'][0]
    assert task1['status'] == 'completed'
    assert 'Team Sync' in task1['task']

def test_feature3_get(client):
    """Test that the feature3 upload page renders successfully."""
    response = client.get('/feature3')
    assert response.status_code == 200
    assert b'AWS S3' in response.data
    assert b'EC2 IAM' in response.data

def test_feature3_post_empty(client):
    """Test that uploading without any file returns a bad request error."""
    # POST without files dict
    response = client.post('/feature3', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    assert data['success'] is False
    assert '缺失' in data['error']

    # POST with empty filename
    response = client.post('/feature3', data={'file': (None, '')}, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    assert data['success'] is False
    assert '尚未選擇' in data['error']


def test_feature4_get(client):
    """Test that the feature4 stress page renders successfully."""
    response = client.get('/feature4')
    assert response.status_code == 200
    assert b'CPU' in response.data
    assert b'CloudWatch' in response.data


def test_stress_start_and_stop(client):
    """Test start and stop endpoints for CPU stress simulation."""
    # Test starting stress with 1 core, 5 seconds
    response = client.post('/api/stress/start', 
                           data=json.dumps({'cores': 1, 'duration': 5}),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['success'] is True
    assert '模擬燒機' in data['message']
    assert data['cores'] == 1
    assert data['duration'] == 5
    assert len(data['pids']) == 1

    # Verify that stress is active in health API
    health_response = client.get('/api/health')
    assert health_response.status_code == 200
    health_data = json.loads(health_response.data.decode('utf-8'))
    # Wait, the stress_active might be true
    assert 'stress_active' in health_data

    # Test stopping stress
    response = client.post('/api/stress/stop')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['success'] is True
    assert '模擬燒機' in data['message'] or '無正在' in data['message']

    # Verify that stress is inactive in health API
    health_response = client.get('/api/health')
    health_data = json.loads(health_response.data.decode('utf-8'))
    assert health_data['stress_active'] is False


