import pytest
from server import app

@pytest.fixture
def client():
    # put Flask into testing mode
    app.testing = True
    with app.test_client() as client:
        yield client

def test_famous_person_endpoint(client):
    """
    Verify /famous-person returns 200 and correct JSON structure.
    """
    resp = client.post(
        '/famous-person',
        json={'message': 'TestUser'}
    )
    assert resp.status_code == 200, "Expected HTTP 200"
    data = resp.get_json()
    # Check keys and values
    assert data.get('famous_person') == 'TestUser'
    assert 'quest' in data
    assert 'Create a quest inspired by TestUser.' in data['quest']

def test_honored_one_endpoint(client):
    """
    Verify /honored_one returns 200 and correct JSON structure.
    """
    # Note: the server expects "message_name", not "honored_one"
    resp = client.post(
        '/honored_one',
        json={'message_name': 'TestHero'}
    )
    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}"
    data = resp.get_json()
    # Make sure the response echoes back our TestHero name
    assert data.get('honored_one') == 'TestHero'
    # And that it includes a quest field
    assert 'quest' in data
    assert f"Create a quest inspired by TestHero." in data['quest']