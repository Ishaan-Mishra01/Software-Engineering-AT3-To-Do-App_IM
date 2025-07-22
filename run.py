#!/usr/bin/env python3
"""
Entry point for To-Do Application
"""
from app import create_app
from app.databases import db
import os

# Create application instance
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

with app.app_context():
    db.create_all()
    print("Tables created.") #for testing it works


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5001))
    app.run(debug=app.config['DEBUG'], port=port)