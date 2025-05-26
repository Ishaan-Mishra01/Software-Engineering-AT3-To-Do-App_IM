"""
Data models and storage functions for To-Do Application
"""
import os
import json
from flask import current_app

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