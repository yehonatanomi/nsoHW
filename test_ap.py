import pytest
from controller import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_message(client):
    data = {
        "application_id": 1,
        "session_id": "abc123",
        "message_id": "msg456",
        "participants": ["user1", "user2"],
        "content": "Hello, world!"
    }
    response = client.post('/AddMessage', json=data)
    assert response.status_code in (200, 201)  # Expecting either 200 or 201
    assert response.get_json() == {'message': 'Message added successfully'}

def test_add_message_2(client):
    data = {
        "application_id": 3,
        "session_id": "abc1234",
        "message_id": "msg4567",
        "participants": ["user1", "user2"],
        "content": ""
    }
    response = client.post('/AddMessage', json=data)
    assert response.status_code in (200, 201)  # Expecting either 200 or 201
    assert response.get_json() == {'message': 'Message added successfully'}
def test_add_message_3(client):
    data = {
        "application_id": 4,
        "session_id": "abc1235",
        "message_id": "msg4566",
        "participants": ["user1", "user2"],
        "content": "Hello, world!"
    }
    response = client.post('/AddMessage', json=data)
    assert response.status_code in (200, 201)  # Expecting either 200 or 201
    assert response.get_json() == {'message': 'Message added successfully'}
def test_get_message_by_application_id(client):
    # Assuming you have added some messages to the database
    response = client.get('/GetMessage?applicationId=1')
    assert response.status_code in (200, 201)
    messages = response.get_json()
    assert len(messages) > 0
def test_get_message_by_application_id_not_exist(client):
    # Assuming you have added some messages to the database
    response = client.get('/GetMessage?applicationId=2')
    assert response.status_code in (200, 201) # Status code should be 200
    messages = response.get_json()
    assert len(messages) == 0  # Ensure the response is an empty list

def test_get_message_by_session_id(client):
    # Assuming you have added some messages to the database
    response = client.get('/GetMessage?sessionId=abc123')
    assert response.status_code in (200, 201)
    messages = response.get_json()
    assert len(messages) > 0
def test_get_message_by_message_id(client):
    # Assuming you have added some messages to the database
    response = client.get('/GetMessage?messageId=msg456')
    assert response.status_code in (200, 201)
    messages = response.get_json()
    assert len(messages) > 0
def test_delete_message_by_session_id(client):
    # Assuming you have added a message to the database
    response = client.delete('/DeleteMessage?sessionId=abc1234')
    assert response.status_code in (200, 201)
    assert response.get_json() == {'message': 'Messages deleted successfully'}
def test_delete_message_by_application_id(client):
    # Assuming you have added a message to the database
    response = client.delete('/DeleteMessage?applicationId=1')
    assert response.status_code in (200, 201)
    assert response.get_json() == {'message': 'Messages deleted successfully'}
def test_delete_message_by_message_id(client):
    # Assuming you have added a message to the database
    response = client.delete('/DeleteMessage?messageId=msg4566')
    assert response.status_code in (200, 201)
    assert response.get_json() == {'message': 'Messages deleted successfully'}
def test_get_message_without_parameter(client):
    # Assuming you have added some messages to the database
    response = client.get('/GetMessage?')
    assert response.status_code ==405 # Status code should be 200
def test_delete_message_without_parameter(client):
    # Assuming you have added a message to the database
    response = client.delete('/DeleteMessage?')
    assert response.get_json() == {'error': 'Invalid parameters'}


if __name__ == '__main__':
    pytest.main()
