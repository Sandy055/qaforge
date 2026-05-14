"""
test_filtering.py
Automated tests for the Task Filtering and Dashboard modules.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from todo_app import app, users, tasks, task_counter


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_data():
    users.clear()
    tasks.clear()
    task_counter[0] = 0
    yield
    users.clear()
    tasks.clear()
    task_counter[0] = 0


def register_user(client, username='testuser'):
    client.post('/register', json={'username': username, 'password': 'pass123'})


def create_task(client, title='Task', username='testuser',
                priority='high', status=None):
    r = client.post('/tasks', json={
        'title': title,
        'username': username,
        'priority': priority
    })
    if status and r.status_code == 201:
        task_id = r.json['task_id']
        client.put(f'/tasks/{task_id}', json={'status': status})
    return r


class TestFilterByStatus:

    def test_filter_by_status_pending(self, client):
        register_user(client)
        create_task(client, title='T1', status='pending')
        create_task(client, title='T2', status='completed')
        response = client.get('/tasks/filter?status=pending')
        assert response.status_code == 200
        assert response.json['count'] == 1
        assert response.json['tasks'][0]['status'] == 'pending'

    def test_filter_by_status_completed(self, client):
        register_user(client)
        create_task(client, title='T1', status='pending')
        create_task(client, title='T2', status='completed')
        response = client.get('/tasks/filter?status=completed')
        assert response.status_code == 200
        assert response.json['count'] == 1
        assert response.json['tasks'][0]['status'] == 'completed'

    def test_filter_by_status_in_progress(self, client):
        register_user(client)
        create_task(client, title='T1', status='in_progress')
        create_task(client, title='T2', status='pending')
        response = client.get('/tasks/filter?status=in_progress')
        assert response.status_code == 200
        assert response.json['count'] == 1

    def test_filter_invalid_status_returns_400(self, client):
        response = client.get('/tasks/filter?status=unknown')
        assert response.status_code == 400

    def test_filter_no_matching_status_returns_empty(self, client):
        register_user(client)
        create_task(client, title='T1', status='pending')
        response = client.get('/tasks/filter?status=completed')
        assert response.status_code == 200
        assert response.json['count'] == 0
        assert response.json['tasks'] == []


class TestFilterByPriority:

    def test_filter_by_priority_high(self, client):
        register_user(client)
        create_task(client, title='T1', priority='high')
        create_task(client, title='T2', priority='low')
        response = client.get('/tasks/filter?priority=high')
        assert response.status_code == 200
        assert response.json['count'] == 1
        assert response.json['tasks'][0]['priority'] == 'high'

    def test_filter_by_priority_low(self, client):
        register_user(client)
        create_task(client, title='T1', priority='high')
        create_task(client, title='T2', priority='low')
        response = client.get('/tasks/filter?priority=low')
        assert response.status_code == 200
        assert response.json['count'] == 1

    def test_filter_by_priority_medium(self, client):
        register_user(client)
        create_task(client, title='T1', priority='medium')
        create_task(client, title='T2', priority='high')
        response = client.get('/tasks/filter?priority=medium')
        assert response.status_code == 200
        assert response.json['count'] == 1

    def test_filter_invalid_priority_returns_400(self, client):
        response = client.get('/tasks/filter?priority=urgent')
        assert response.status_code == 400


class TestFilterByUsername:

    def test_filter_by_username(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        create_task(client, title='T1', username='user1')
        create_task(client, title='T2', username='user2')
        response = client.get('/tasks/filter?username=user1')
        assert response.status_code == 200
        assert response.json['count'] == 1
        assert response.json['tasks'][0]['username'] == 'user1'

    def test_filter_username_does_not_show_other_users_tasks(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        create_task(client, title='T1', username='user1')
        create_task(client, title='T2', username='user2')
        response = client.get('/tasks/filter?username=user1')
        for task in response.json['tasks']:
            assert task['username'] == 'user1'


class TestCombinedFilters:

    def test_filter_by_status_and_priority(self, client):
        register_user(client)
        create_task(client, title='T1', priority='high', status='pending')
        create_task(client, title='T2', priority='low', status='pending')
        create_task(client, title='T3', priority='high', status='completed')
        response = client.get('/tasks/filter?status=pending&priority=high')
        assert response.status_code == 200
        assert response.json['count'] == 1

    def test_filter_all_three_parameters(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        create_task(client, title='T1', username='user1',
                    priority='high', status='pending')
        create_task(client, title='T2', username='user2',
                    priority='high', status='pending')
        response = client.get(
            '/tasks/filter?status=pending&priority=high&username=user1')
        assert response.status_code == 200
        assert response.json['count'] == 1
        assert response.json['tasks'][0]['username'] == 'user1'


class TestDashboard:

    def test_dashboard_valid_user_returns_200(self, client):
        register_user(client)
        response = client.get('/dashboard?username=testuser')
        assert response.status_code == 200

    def test_dashboard_no_tasks_all_counts_zero(self, client):
        register_user(client)
        response = client.get('/dashboard?username=testuser')
        data = response.json
        assert data['total'] == 0
        assert data['pending'] == 0
        assert data['in_progress'] == 0
        assert data['completed'] == 0
        assert data['high_priority'] == 0

    def test_dashboard_nonexistent_user_returns_404(self, client):
        response = client.get('/dashboard?username=ghost')
        assert response.status_code == 404

    def test_dashboard_without_username_returns_400(self, client):
        response = client.get('/dashboard')
        assert response.status_code == 400

    def test_dashboard_pending_count_correct(self, client):
        register_user(client)
        create_task(client, title='T1', status='pending')
        create_task(client, title='T2', status='pending')
        create_task(client, title='T3', status='completed')
        response = client.get('/dashboard?username=testuser')
        assert response.json['pending'] == 2
        assert response.json['completed'] == 1

    def test_dashboard_high_priority_count_correct(self, client):
        register_user(client)
        create_task(client, title='T1', priority='high')
        create_task(client, title='T2', priority='high')
        create_task(client, title='T3', priority='low')
        response = client.get('/dashboard?username=testuser')
        assert response.json['high_priority'] == 2

    def test_dashboard_total_count_correct(self, client):
        register_user(client)
        create_task(client, title='T1')
        create_task(client, title='T2')
        create_task(client, title='T3')
        response = client.get('/dashboard?username=testuser')
        assert response.json['total'] == 3

    def test_dashboard_updates_after_task_completed(self, client):
        register_user(client)
        r = create_task(client, title='T1')
        task_id = r.json['task_id']
        before = client.get('/dashboard?username=testuser').json
        client.put(f'/tasks/{task_id}', json={'status': 'completed'})
        after = client.get('/dashboard?username=testuser').json
        assert after['completed'] == before['completed'] + 1
        assert after['pending'] == before['pending'] - 1

    def test_dashboard_updates_after_task_deleted(self, client):
        register_user(client)
        r = create_task(client, title='T1')
        task_id = r.json['task_id']
        before = client.get('/dashboard?username=testuser').json
        client.delete(f'/tasks/{task_id}')
        after = client.get('/dashboard?username=testuser').json
        assert after['total'] == before['total'] - 1

    def test_dashboard_only_shows_own_tasks(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        create_task(client, title='T1', username='user1')
        create_task(client, title='T2', username='user1')
        create_task(client, title='T3', username='user2')
        response = client.get('/dashboard?username=user1')
        assert response.json['total'] == 2
