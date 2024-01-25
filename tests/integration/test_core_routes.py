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

def test_getting_blog_post(client):
    """Test getting a blog post."""
    running_blog_post_route = "/blog/post/1"
    response = client.get(running_blog_post_route)
    assert response.status_code == 200
    assert "Goals 2024 - Running" in str(response.data)
