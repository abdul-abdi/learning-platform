import json
from flask_jwt_extended import create_access_token
from app.models.user import User

def test_user_registration(client, init_database):
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_user_login(client, init_database):
    # First, register a user
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    # Then, try to login
    response = client.post('/auth/login', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data)

def test_invalid_login(client, init_database):
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data