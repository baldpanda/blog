import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Test the home page route."""
    response = client.get('/blog/')
    assert response.status_code == 200
