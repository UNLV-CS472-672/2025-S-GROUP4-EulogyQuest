# ai-gen start (ChatGPT-4, 1)
# tests/test_server.py

import pytest
from website.server.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_famous_person_no_data(client):
    # Send POST request without any data
    response = client.post('/famous-person', json={})
    
    # Verify response
    assert response.status_code == 400
    assert response.get_json() == {
        'error': 'Invalid request: "message" field is required and cannot be empty'
    }
# ai-gen end

def test_post_famous_person_valid_data(client):
    # Send POST request with data
    response = client.post('/famous-person', json={'message': 'George Washington'})

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert 'famous_person' in data
    assert data['famous_person'] == 'George Washington'
    assert 'quest' in data
    assert data['quest'] == 'Create a quest inspired by George Washington.'

def test_post_honored_one_no_data(client):
    # Send POST request without any data
    response = client.post('/honored_one', json={})
    
    # Verify response
    assert response.status_code == 400
    assert response.get_json() == {
        'error': 'Invalid request: "name" field is required and cannot be empty'
    }

def test_post_honored_one_valid_data(client):
    # Send POST request with data
    response = client.post('/honored_one', json={'message_name': 'Abraham Lincoln', 'message_logs': None})

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert 'honored_one' in data
    assert data['honored_one'] == 'Abraham Lincoln'
    assert 'quest' in data
    assert data['quest'] == 'Create a quest inspired by Abraham Lincoln.'
