"""
test_regression.py
Regression test suite for ToDoApp.
Verifies that changes to one part of the system do not break other parts.
These tests are run on every build to catch unintended side effects.
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


def create_task(client, title='Task', username='testuser', priority='high'):
    return client.post('/tasks', json={
        'title': title,
        'username': username,
        'priority': priority
    })


class TestAuthRegression:

    def test_registering_new_user_does_not_affect_existing_users(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        response = client.post('/login', json={
            'username': 'user1',
            'password': 'pass123'
        })
        assert response.status_code == 200

    def test_failed_login_does_not_lock_out_valid_login(self, client):
        register_user(client)
        client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpass'
        })
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'pass123'
        })
        assert response.status_code == 200

    def test_logout_does_not_delete_user(self, client):
        register_user(client)
        client.post('/logout', json={'username': 'testuser'})
        response = client.post('/login', json={
            'username': 'testuser',
            'password': 'pass123'
        })
        assert response.status_code == 200


class TestTaskRegression:

    def test_creating_task_does_not_affect_other_tasks(self, client):
        register_user(client)
        r1 = create_task(client, title='Task 1')
        create_task(client, title='Task 2')
        task_id_1 = r1.json['task_id']
        response = client.get(f'/tasks/{task_id_1}')
        assert response.json['title'] == 'Task 1'

    def test_updating_task_does_not_affect_other_tasks(self, client):
        register_user(client)
        r1 = create_task(client, title='Task 1')
        r2 = create_task(client, title='Task 2')
        task_id_1 = r1.json['task_id']
        task_id_2 = r2.json['task_id']
        client.put(f'/tasks/{task_id_1}', json={'title': 'Updated Task 1'})
        response = client.get(f'/tasks/{task_id_2}')
        assert response.json['title'] == 'Task 2'

    def test_deleting_task_does_not_affect_other_tasks(self, client):
        register_user(client)
        r1 = create_task(client, title='Task 1')
        r2 = create_task(client, title='Task 2')
        task_id_1 = r1.json['task_id']
        task_id_2 = r2.json['task_id']
        client.delete(f'/tasks/{task_id_1}')
        response = client.get(f'/tasks/{task_id_2}')
        assert response.status_code == 200
        assert response.json['title'] == 'Task 2'

    def test_deleting_user_tasks_does_not_delete_other_user_tasks(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        r1 = create_task(client, title='User1 Task', username='user1')
        r2 = create_task(client, title='User2 Task', username='user2')
        task_id_1 = r1.json['task_id']
        task_id_2 = r2.json['task_id']
        client.delete(f'/tasks/{task_id_1}')
        response = client.get(f'/tasks/{task_id_2}')
        assert response.status_code == 200

    def test_task_status_update_does_not_change_other_fields(self, client):
        register_user(client)
        r = create_task(client, title='My Task', priority='high')
        task_id = r.json['task_id']
        client.put(f'/tasks/{task_id}', json={'status': 'completed'})
        response = client.get(f'/tasks/{task_id}')
        assert response.json['title'] == 'My Task'
        assert response.json['priority'] == 'high'
        assert response.json['status'] == 'completed'

    def test_task_priority_update_does_not_change_other_fields(self, client):
        register_user(client)
        r = create_task(client, title='My Task', priority='low')
        task_id = r.json['task_id']
        client.put(f'/tasks/{task_id}', json={'priority': 'high'})
        response = client.get(f'/tasks/{task_id}')
        assert response.json['title'] == 'My Task'
        assert response.json['priority'] == 'high'
        assert response.json['status'] == 'pending'


class TestFilterRegression:

    def test_filter_results_not_affected_by_other_users_tasks(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        create_task(client, title='T1', username='user1', priority='high')
        create_task(client, title='T2', username='user2', priority='high')
        response = client.get('/tasks/filter?username=user1&priority=high')
        assert response.json['count'] == 1

    def test_filter_count_updates_after_task_deleted(self, client):
        register_user(client)
        r = create_task(client, title='T1', priority='high')
        task_id = r.json['task_id']
        before = client.get('/tasks/filter?priority=high').json['count']
        client.delete(f'/tasks/{task_id}')
        after = client.get('/tasks/filter?priority=high').json['count']
        assert after == before - 1

    def test_filter_count_updates_after_task_status_changed(self, client):
        register_user(client)
        r = create_task(client, title='T1')
        task_id = r.json['task_id']
        before = client.get('/tasks/filter?status=pending').json['count']
        client.put(f'/tasks/{task_id}', json={'status': 'completed'})
        after = client.get('/tasks/filter?status=pending').json['count']
        assert after == before - 1


class TestDashboardRegression:

    def test_dashboard_not_affected_by_other_users(self, client):
        register_user(client, username='user1')
        register_user(client, username='user2')
        create_task(client, title='T1', username='user1')
        create_task(client, title='T2', username='user2')
        create_task(client, title='T3', username='user2')
        response = client.get('/dashboard?username=user1')
        assert response.json['total'] == 1

    def test_dashboard_consistent_with_filter(self, client):
        register_user(client)
        create_task(client, title='T1', priority='high')
        create_task(client, title='T2', priority='high')
        create_task(client, title='T3', priority='low')
        dashboard = client.get('/dashboard?username=testuser').json
        filter_high = client.get(
            '/tasks/filter?priority=high&username=testuser').json
        assert dashboard['high_priority'] == filter_high['count']

    def test_dashboard_total_consistent_with_all_tasks(self, client):
        register_user(client)
        create_task(client, title='T1')
        create_task(client, title='T2')
        create_task(client, title='T3')
        dashboard = client.get('/dashboard?username=testuser').json
        all_tasks = client.get(
            '/tasks/filter?username=testuser').json
        assert dashboard['total'] == all_tasks['count']


class TestEndToEndRegression:

    def test_full_task_lifecycle(self, client):
        register_user(client)
        r = create_task(client, title='Complete me')
        task_id = r.json['task_id']
        client.put(f'/tasks/{task_id}', json={'status': 'in_progress'})
        response = client.get(f'/tasks/{task_id}')
        assert response.json['status'] == 'in_progress'
        client.put(f'/tasks/{task_id}', json={'status': 'completed'})
        response = client.get(f'/tasks/{task_id}')
        assert response.json['status'] == 'completed'
        client.delete(f'/tasks/{task_id}')
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 404

    def test_multiple_users_isolated(self, client):
        register_user(client, username='alice')
        register_user(client, username='bob')
        create_task(client, title='Alice task', username='alice')
        create_task(client, title='Bob task', username='bob')
        alice_dash = client.get('/dashboard?username=alice').json
        bob_dash = client.get('/dashboard?username=bob').json
        assert alice_dash['total'] == 1
        assert bob_dash['total'] == 1

    def test_register_login_create_task_view_dashboard(self, client):
        client.post('/register', json={
            'username': 'newuser',
            'password': 'secure123'
        })
        login = client.post('/login', json={
            'username': 'newuser',
            'password': 'secure123'
        })
        assert login.status_code == 200
        create_task(client, title='First task', username='newuser')
        dashboard = client.get('/dashboard?username=newuser').json
        assert dashboard['total'] == 1
        assert dashboard['pending'] == 1
