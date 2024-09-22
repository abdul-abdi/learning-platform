import pytest
from flask_jwt_extended import create_access_token
from app.models.user import User

def test_register(client, init_database):
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_login(client, init_database):
    # First, register a user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    # Then, try to login
    response = client.post('/api/auth/login', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_protected_route(client, init_database):
    # Register and login a user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    login_response = client.post('/api/auth/login', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    token = login_response.json['access_token']

    # Test a protected route
    response = client.get('/api/protected', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert b'Access granted' in response.data

def test_invalid_login(client, init_database):
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data