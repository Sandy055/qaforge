"""
todo_app.py
A simple task management web application.
This is the application QAForge tests against.
Modules: Authentication, Task Management, Task Filtering, Dashboard
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory stores
users = {}
tasks = {}
task_counter = [0]


# ─────────────────────────────────────────────
# AUTH MODULE
# ─────────────────────────────────────────────

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    if len(data['username'].strip()) == 0:
        return jsonify({'error': 'Username cannot be empty'}), 400
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if data['username'] in users:
        return jsonify({'error': 'Username already exists'}), 409
    users[data['username']] = {
        'username': data['username'],
        'password': data['password']
    }
    return jsonify({'message': 'User registered', 'username': data['username']}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    if data['username'] not in users:
        return jsonify({'error': 'User not found'}), 404
    if users[data['username']]['password'] != data['password']:
        return jsonify({'error': 'Invalid password'}), 401
    return jsonify({'message': 'Login successful', 'username': data['username']}), 200


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'error': 'Username required'}), 400
    if data['username'] not in users:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'Logout successful'}), 200


# ─────────────────────────────────────────────
# TASK MANAGEMENT MODULE
# ─────────────────────────────────────────────

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required = ['title', 'username', 'priority']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    if len(data['title'].strip()) == 0:
        return jsonify({'error': 'Title cannot be empty'}), 400
    if data['priority'] not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Priority must be low, medium, or high'}), 400
    if data['username'] not in users:
        return jsonify({'error': 'User not found'}), 404
    task_counter[0] += 1
    task_id = f'T{task_counter[0]:03d}'
    tasks[task_id] = {
        'task_id': task_id,
        'title': data['title'].strip(),
        'username': data['username'],
        'priority': data['priority'],
        'status': 'pending',
        'due_date': data.get('due_date', None)
    }
    return jsonify({'message': 'Task created', 'task_id': task_id}), 201


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(tasks[task_id]), 200


@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'title' in data:
        if len(data['title'].strip()) == 0:
            return jsonify({'error': 'Title cannot be empty'}), 400
        tasks[task_id]['title'] = data['title'].strip()
    if 'priority' in data:
        if data['priority'] not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Priority must be low, medium, or high'}), 400
        tasks[task_id]['priority'] = data['priority']
    if 'status' in data:
        if data['status'] not in ['pending', 'in_progress', 'completed']:
            return jsonify({'error': 'Status must be pending, in_progress, or completed'}), 400
        tasks[task_id]['status'] = data['status']
    if 'due_date' in data:
        tasks[task_id]['due_date'] = data['due_date']
    return jsonify({'message': 'Task updated', 'task': tasks[task_id]}), 200


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    del tasks[task_id]
    return jsonify({'message': 'Task deleted', 'task_id': task_id}), 200


@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify({'tasks': list(tasks.values()), 'count': len(tasks)}), 200


# ─────────────────────────────────────────────
# FILTERING MODULE
# ─────────────────────────────────────────────

@app.route('/tasks/filter', methods=['GET'])
def filter_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority')
    username = request.args.get('username')
    filtered = list(tasks.values())
    if status:
        if status not in ['pending', 'in_progress', 'completed']:
            return jsonify({'error': 'Invalid status filter'}), 400
        filtered = [t for t in filtered if t['status'] == status]
    if priority:
        if priority not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Invalid priority filter'}), 400
        filtered = [t for t in filtered if t['priority'] == priority]
    if username:
        filtered = [t for t in filtered if t['username'] == username]
    return jsonify({'tasks': filtered, 'count': len(filtered)}), 200


# ─────────────────────────────────────────────
# DASHBOARD MODULE
# ─────────────────────────────────────────────

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400
    if username not in users:
        return jsonify({'error': 'User not found'}), 404
    user_tasks = [t for t in tasks.values() if t['username'] == username]
    summary = {
        'username': username,
        'total': len(user_tasks),
        'pending': len([t for t in user_tasks if t['status'] == 'pending']),
        'in_progress': len([t for t in user_tasks if t['status'] == 'in_progress']),
        'completed': len([t for t in user_tasks if t['status'] == 'completed']),
        'high_priority': len([t for t in user_tasks if t['priority'] == 'high'])
    }
    return jsonify(summary), 200


if __name__ == '__main__':
    app.run(debug=True, port=5051)
