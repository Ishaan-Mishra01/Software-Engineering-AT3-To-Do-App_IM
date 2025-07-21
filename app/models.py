"""
Data models and storage functions for To-Do Application
"""
import os
import json
from flask import current_app
from datetime import datetime, timedelta

def get_data_file():
    """Get the data file path from config"""
    return current_app.config.get('DATA_FILE', 'data.json')

def load_data():
    """Load data from JSON file"""
    data_file = get_data_file()
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {'users': {}, 'tasks': {}}

def save_data(data):
    """Save data to JSON file"""
    data_file = get_data_file()
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)


def cleanup_old_completed_tasks(user_email, days_old=30):
    """Remove completed tasks older than specified days"""
    data = load_data()
    
    if user_email not in data['tasks']:
        return 0
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    original_count = len(data['tasks'][user_email])
    
    # Filter out old completed tasks
    data['tasks'][user_email] = [
        task for task in data['tasks'][user_email]
        if not (
            task.get('completed', False) and 
            task.get('completed_date') and
            datetime.fromisoformat(task['completed_date']) < cutoff_date
        )
    ]
    
    removed_count = original_count - len(data['tasks'][user_email])
    
    if removed_count > 0:
        save_data(data)
    
    return removed_count


def mark_task_completed(user_email, task_id):
    """Mark a task as completed and add completion timestamp"""
    data = load_data()
    
    if user_email not in data['tasks']:
        return False
    
    for task in data['tasks'][user_email]:
        if task['id'] == task_id:
            task['completed'] = True
            task['completed_date'] = datetime.now().isoformat()
            save_data(data)
            return True
    
    return False