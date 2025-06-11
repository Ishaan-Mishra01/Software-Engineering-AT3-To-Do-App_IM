"""
Routes for To-Do Application
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from app.models import load_data, save_data, cleanup_old_completed_tasks, mark_task_completed
from app.chatbot import get_chatbot_response, format_chatbot_response
import calendar

main = Blueprint('main', __name__)
calendar_routes = Blueprint('calendar_routes', __name__)

@main.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return redirect(url_for('main.home'))

@main.route('/home')
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
        # Cleanup old completed tasks before returning
        cleanup_old_completed_tasks(user_email)
        
        # Reload data after cleanup
        data = load_data()
        user_tasks = data['tasks'].get(user_email, [])
        return jsonify(user_tasks)
    
    elif request.method == 'POST':
        task_data = request.json
        new_task = {
            'id': str(datetime.now().timestamp()),
            'text': task_data['text'],
            'completed': False,
            'list': task_data.get('list', 'All Tasks'),
            'due_date': task_data.get('due_date'),
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
                # If marking as completed, add completion timestamp
                if task_update.get('completed') and not task.get('completed'):
                    task_update['completed_date'] = datetime.now().isoformat()
                # If marking as not completed, remove completion timestamp
                elif not task_update.get('completed', True) and task.get('completed'):
                    task_update['completed_date'] = None
                    
                task.update(task_update)
                save_data(data)
                return jsonify(task)
        return jsonify({'error': 'Task not found'}), 404
    
    elif request.method == 'DELETE':
        data['tasks'][user_email] = [t for t in user_tasks if t['id'] != task_id]
        save_data(data)
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
    """Manually trigger cleanup of old completed tasks"""
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_email = session['email']
    removed_count = cleanup_old_completed_tasks(user_email)
    
    return jsonify({
        'message': f'Removed {removed_count} old completed tasks',
        'removed_count': removed_count
    })