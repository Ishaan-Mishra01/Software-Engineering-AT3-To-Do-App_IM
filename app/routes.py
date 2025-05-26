"""
Routes for To-Do Application
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from app.models import load_data, save_data

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', username=session['user'])

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        data = load_data()
        
        # Simple registration/login logic
        if email in data['users']:
            # Check login
            if data['users'][email]['password'] == password:
                session['user'] = data['users'][email]['username']
                session['email'] = email
                return redirect(url_for('main.home'))
            else:
                return render_template('login.html', error='Invalid credentials')
        else:
            # Register new user
            data['users'][email] = {
                'username': username,
                'password': password,
                'created': datetime.now().isoformat()
            }
            data['tasks'][email] = []
            save_data(data)
            session['user'] = username
            session['email'] = email
            return redirect(url_for('main.home'))
    
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('main.login'))

@main.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = load_data()
    user_email = session['email']
    
    if request.method == 'GET':
        user_tasks = data['tasks'].get(user_email, [])
        return jsonify(user_tasks)
    
    elif request.method == 'POST':
        task_data = request.json
        new_task = {
            'id': str(datetime.now().timestamp()),
            'text': task_data['text'],
            'completed': False,
            'list': task_data.get('list', 'All Tasks'),
            'created': datetime.now().isoformat()
        }
        
        if user_email not in data['tasks']:
            data['tasks'][user_email] = []
        
        data['tasks'][user_email].append(new_task)
        save_data(data)
        return jsonify(new_task)

@main.route('/api/tasks/<task_id>', methods=['PUT', 'DELETE'])
def task_detail(task_id):
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = load_data()
    user_email = session['email']
    user_tasks = data['tasks'].get(user_email, [])
    
    if request.method == 'PUT':
        task_update = request.json
        for task in user_tasks:
            if task['id'] == task_id:
                task.update(task_update)
                save_data(data)
                return jsonify(task)
        return jsonify({'error': 'Task not found'}), 404
    
    elif request.method == 'DELETE':
        data['tasks'][user_email] = [t for t in user_tasks if t['id'] != task_id]
        save_data(data)
        return jsonify({'success': True})