"""
test_auth.py
Automated tests for the Authentication module.
Covers registration, login, and logout endpoints.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from todo_app import app, users, tasks


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_data():
    users.clear()
    tasks.clear()
    yield
    users.clear()
    tasks.clear()


def register_user(client, username='testuser', password='pass123'):
    return client.post('/register', json={
        'username': username,
        'password': password
    })


class TestRegistration:

    def test_register_valid_user_returns_201(self, client):
        response = register_user(client)
        assert response.status_code == 201
        assert response.json['message'] == 'User registered'
        assert response.json['username'] == 'testuser'

    def test_register_duplicate_username_returns_409(self, client):
        register_user(client)
        response = register_user(client)
        assert response.status_code == 409
        assert 'already exists' in response.json['error']

    def test_register_short_password_returns_400(self, client):
        response = register_user(client, password='abc')
        assert response.status_code == 400
        assert 'Password' in response.json['error']

    def test_register_empty_username_returns_400(self, client):
        response = register_user(client, username='')
        assert response.status_code == 400

    def test_register_whitespace_username_returns_400(self, client):
        response = register_user(client, username='   ')
        assert response.status_code == 400

    def test_register_missing_username_returns_400(self, client):
        response = client.post('/register', json={'password': 'pass123'})
        assert response.status_code == 400

    def test_register_missing_password_returns_400(self, client):
        response = client.post('/register', json={'username': 'testuser'})
        assert response.status_code == 400

    def test_register_no_body_returns_400(self, client):
        response = client.post('/register', json=None,
                               content_type='application/json')
        assert response.status_code == 400

    def test_register_password_exactly_6_chars_accepted(self, client):
        response = register_user(client, password='abc123')
        assert response.status_code == 201

    def test_register_password_exactly_5_chars_rejected(self, client):
        response = register_user(client, password='abc12')
        assert response.status_code == 400

    def test_register_multiple_different_users(self, client):
        r1 = register_user(client, username='user1')
        r2 = register_user(client, username='user2')
        assert r1.status_code == 201
        assert r2.status_code == 201


class TestLogin:

    def test_login_valid_credentials_returns_200(self, client):
        register_user(client)
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'pass123'
        })
        assert response.status_code == 200
        assert response.json['message'] == 'Login successful'

    def test_login_wrong_password_returns_401(self, client):
        register_user(client)
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpass'
        })
        assert response.status_code == 401
        assert 'Invalid password' in response.json['error']

    def test_login_nonexistent_user_returns_404(self, client):
        response = client.post('/login', json={
            'username': 'ghost',
            'password': 'pass123'
        })
        assert response.status_code == 404

    def test_login_missing_password_returns_400(self, client):
        response = client.post('/login', json={'username': 'testuser'})
        assert response.status_code == 400

    def test_login_missing_username_returns_400(self, client):
        response = client.post('/login', json={'password': 'pass123'})
        assert response.status_code == 400

    def test_login_empty_body_returns_400(self, client):
        response = client.post('/login', json=None,
                               content_type='application/json')
        assert response.status_code == 400

    def test_login_returns_username_in_response(self, client):
        register_user(client)
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'pass123'
        })
        assert response.json['username'] == 'testuser'


class TestLogout:

    def test_logout_existing_user_returns_200(self, client):
        register_user(client)
        response = client.post('/logout', json={'username': 'testuser'})
        assert response.status_code == 200
        assert response.json['message'] == 'Logout successful'

    def test_logout_nonexistent_user_returns_404(self, client):
        response = client.post('/logout', json={'username': 'ghost'})
        assert response.status_code == 404

    def test_logout_missing_username_returns_400(self, client):
        response = client.post('/logout', json={})
        assert response.status_code == 400
