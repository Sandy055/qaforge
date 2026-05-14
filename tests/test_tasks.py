"""
test_tasks.py
Automated tests for the Task Management module.
Covers create, read, update, and delete operations.
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
    client.post('/register', json={
        'username': username,
        'password': 'pass123'
    })


def create_task(client, title='Buy groceries', username='testuser',
                priority='high', due_date=None):
    payload = {'title': title, 'username': username, 'priority': priority}
    if due_date:
        payload['due_date'] = due_date
    return client.post('/tasks', json=payload)


class TestCreateTask:

    def test_create_valid_task_returns_201(self, client):
        register_user(client)
        response = create_task(client)
        assert response.status_code == 201
        assert response.json['message'] == 'Task created'
        assert 'task_id' in response.json

    def test_create_task_missing_title_returns_400(self, client):
        register_user(client)
        response = client.post('/tasks', json={
            'username': 'testuser',
            'priority': 'high'
        })
        assert response.status_code == 400

    def test_create_task_missing_username_returns_400(self, client):
        register_user(client)
        response = client.post('/tasks', json={
            'title': 'Buy groceries',
            'priority': 'high'
        })
        assert response.status_code == 400

    def test_create_task_missing_priority_returns_400(self, client):
        register_user(client)
        response = client.post('/tasks', json={
            'title': 'Buy groceries',
            'username': 'testuser'
        })
        assert response.status_code == 400

    def test_create_task_invalid_priority_returns_400(self, client):
        register_user(client)
        response = create_task(client, priority='urgent')
        assert response.status_code == 400

    def test_create_task_empty_title_returns_400(self, client):
        register_user(client)
        response = create_task(client, title='')
        assert response.status_code == 400

    def test_create_task_whitespace_title_returns_400(self, client):
        register_user(client)
        response = create_task(client, title='   ')
        assert response.status_code == 400

    def test_create_task_nonexistent_user_returns_404(self, client):
        response = create_task(client, username='ghost')
        assert response.status_code == 404

    def test_create_task_priority_low_accepted(self, client):
        register_user(client)
        response = create_task(client, priority='low')
        assert response.status_code == 201

    def test_create_task_priority_medium_accepted(self, client):
        register_user(client)
        response = create_task(client, priority='medium')
        assert response.status_code == 201

    def test_create_task_priority_high_accepted(self, client):
        register_user(client)
        response = create_task(client, priority='high')
        assert response.status_code == 201

    def test_create_task_with_due_date(self, client):
        register_user(client)
        response = create_task(client, due_date='2025-12-31')
        assert response.status_code == 201

    def test_create_task_without_due_date_stored_as_none(self, client):
        register_user(client)
        response = create_task(client)
        task_id = response.json['task_id']
        task = client.get(f'/tasks/{task_id}')
        assert task.json['due_date'] is None

    def test_create_task_default_status_is_pending(self, client):
        register_user(client)
        response = create_task(client)
        task_id = response.json['task_id']
        task = client.get(f'/tasks/{task_id}')
        assert task.json['status'] == 'pending'

    def test_create_task_title_whitespace_stripped(self, client):
        register_user(client)
        response = create_task(client, title='  Buy groceries  ')
        task_id = response.json['task_id']
        task = client.get(f'/tasks/{task_id}')
        assert task.json['title'] == 'Buy groceries'


class TestGetTask:

    def test_get_existing_task_returns_200(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200

    def test_get_nonexistent_task_returns_404(self, client):
        response = client.get('/tasks/T999')
        assert response.status_code == 404

    def test_get_task_returns_all_fields(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.get(f'/tasks/{task_id}')
        data = response.json
        assert 'task_id' in data
        assert 'title' in data
        assert 'username' in data
        assert 'priority' in data
        assert 'status' in data
        assert 'due_date' in data

    def test_get_all_tasks_returns_correct_count(self, client):
        register_user(client)
        create_task(client, title='Task 1')
        create_task(client, title='Task 2')
        response = client.get('/tasks')
        assert response.json['count'] == 2


class TestUpdateTask:

    def test_update_task_title_returns_200(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.put(f'/tasks/{task_id}',
                              json={'title': 'Updated title'})
        assert response.status_code == 200
        assert response.json['task']['title'] == 'Updated title'

    def test_update_task_status_to_in_progress(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.put(f'/tasks/{task_id}',
                              json={'status': 'in_progress'})
        assert response.status_code == 200
        assert response.json['task']['status'] == 'in_progress'

    def test_update_task_status_to_completed(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.put(f'/tasks/{task_id}',
                              json={'status': 'completed'})
        assert response.status_code == 200
        assert response.json['task']['status'] == 'completed'

    def test_update_task_invalid_status_returns_400(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.put(f'/tasks/{task_id}',
                              json={'status': 'done'})
        assert response.status_code == 400

    def test_update_task_invalid_priority_returns_400(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.put(f'/tasks/{task_id}',
                              json={'priority': 'critical'})
        assert response.status_code == 400

    def test_update_task_empty_title_returns_400(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.put(f'/tasks/{task_id}', json={'title': ''})
        assert response.status_code == 400

    def test_update_nonexistent_task_returns_404(self, client):
        response = client.put('/tasks/T999', json={'title': 'New title'})
        assert response.status_code == 404

    def test_update_persists_after_get(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        client.put(f'/tasks/{task_id}', json={'title': 'Persisted title'})
        response = client.get(f'/tasks/{task_id}')
        assert response.json['title'] == 'Persisted title'


class TestDeleteTask:

    def test_delete_existing_task_returns_200(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        response = client.delete(f'/tasks/{task_id}')
        assert response.status_code == 200
        assert response.json['message'] == 'Task deleted'

    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.delete('/tasks/T999')
        assert response.status_code == 404

    def test_deleted_task_not_retrievable(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        client.delete(f'/tasks/{task_id}')
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 404

    def test_deleting_one_task_does_not_affect_others(self, client):
        register_user(client)
        r1 = create_task(client, title='Task 1')
        r2 = create_task(client, title='Task 2')
        task_id_1 = r1.json['task_id']
        task_id_2 = r2.json['task_id']
        client.delete(f'/tasks/{task_id_1}')
        response = client.get(f'/tasks/{task_id_2}')
        assert response.status_code == 200

    def test_task_count_decreases_after_deletion(self, client):
        register_user(client)
        r = create_task(client)
        task_id = r.json['task_id']
        client.delete(f'/tasks/{task_id}')
        response = client.get('/tasks')
        assert response.json['count'] == 0
