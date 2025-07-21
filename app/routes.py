"""
Routes for To-Do Application
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime
from app.models import load_data, save_data, cleanup_old_completed_tasks, mark_task_completed
from app.chatbot import get_chatbot_response, format_chatbot_response
import calendar
from app.databases import db, User, Task, cleanup_old_completed_tasks
from app.utils import hash_password
from datetime import datetime

main = Blueprint('main', __name__)
calendar_routes = Blueprint('calendar_routes', __name__)

#Routes:

@main.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return redirect(url_for('main.home'))

@main.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', username=session['user'], active_list='All Tasks')

@main.route('/tasks/all')
def all_tasks():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', username=session['user'], active_list='All Tasks')

@main.route('/tasks/personal')
def personal_tasks():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', username=session['user'], active_list='Personal')

@main.route('/tasks/work')
def work_tasks():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', username=session['user'], active_list='Work')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        hashed_pw = hash_password(password)
        user = User.query.get(email=email, username=username, password=hashed_pw, created=datetime.now()) #I don't really know how to change this created time if the user isn't signing up for first time
        data = load_data()
        
        if user:
            #check if user already registered
            if user.password == hash_password(password):
                session['user'] = user.username
                session['email'] = user.email
                return redirect(url_for('main.home'))
            else:
                return render_template('login.html', error='Invalid credentials')
        else:
            # Register new user
            new_user = User(
                email=email,
                username=username,
                password=hash_password(password),
                created=datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()

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

    user_email = session['email']

    if request.method == 'GET':
        user_tasks = Task.query.filter_by(user_email=user_email).all()
        return jsonify([
            {
                'id': task.id,
                'text': task.text,
                'completed': task.completed,
                'list': task.list,
                'due_date': task.due_date,
                'created': task.created.isoformat(),
                'completed_date': task.completed_date.isoformat() if task.completed_date else None
            } for task in user_tasks
        ])

    elif request.method == 'POST':
        task_data = request.json
        new_task = Task(
            text=task_data['text'],
            list=task_data.get('list', 'All Tasks'),
            due_date=task_data.get('due_date'),
            created=datetime.now(),
            user_email=user_email
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'id': new_task.id,
            'text': new_task.text,
            'completed': new_task.completed,
            'list': new_task.list,
            'due_date': new_task.due_date,
            'created': new_task.created.isoformat()
        })


@main.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task_detail(task_id):
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    task = Task.query.filter_by(id=task_id, user_email=session['email']).first()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'PUT':
        task_data = request.json
        task.text = task_data.get('text', task.text)
        task.list = task_data.get('list', task.list)
        task.due_date = task_data.get('due_date', task.due_date)
        task.completed = task_data.get('completed', task.completed)

        if task_data.get('completed') and not task.completed_date:
            task.completed_date = datetime.now()
        elif not task_data.get('completed') and task.completed_date:
            task.completed_date = None

        db.session.commit()
        return jsonify({'success': True})

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'success': True})

    
@calendar_routes.route('/calendar')
def calendar_view():
    if 'user' not in session:
        return redirect(url_for('main.login'))
        
    try:
        year = int(request.args.get("year", datetime.now().year))
        month = int(request.args.get("month", datetime.now().month))
    except ValueError:
        return "Invalid Arguments", 400

    month_name = calendar.month_name[month]
    cal = calendar.Calendar().monthdatescalendar(year, month)

    # Calculate prev and next month
    if month > 1:
        prev_month = month - 1
        prev_year = year
    else:
        prev_month = 12
        prev_year = year - 1

    if month < 12:
        next_month = month + 1
        next_year = year
    else:
        next_month = 1
        next_year = year + 1
        
    # Get user tasks with due dates
    data = load_data()
    user_email = session.get('email')
    user_tasks = data['tasks'].get(user_email, [])
    
    # Group tasks by due date for calendar display
    tasks_by_date = {}
    for task in user_tasks:
        if task.get('due_date'):
            due_date = task['due_date']
            if due_date not in tasks_by_date:
                tasks_by_date[due_date] = []
            tasks_by_date[due_date].append(task)
    
    return render_template(
        "calendar.html", year=year, month=month, calendar=cal,
        prev_year=prev_year, prev_month=prev_month, 
        next_year=next_year, next_month=next_month,
        month_name=month_name, tasks_by_date=tasks_by_date,
        username=session['user']
    )

@main.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Handle chatbot queries"""
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        user_message = request.json.get('message', '')
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
        
        response_data = get_chatbot_response(user_message)
        formatted_response = format_chatbot_response(response_data)
        
        return jsonify(formatted_response)
    
    except Exception as e:
        return jsonify({'error': 'Chatbot error', 'details': str(e)}), 500

@main.route('/api/cleanup-tasks', methods=['POST'])
def cleanup_tasks():
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    removed_count = cleanup_old_completed_tasks(session['email'])
    return jsonify({
        'message': f'Removed {removed_count} old completed tasks',
        'removed_count': removed_count
    })
