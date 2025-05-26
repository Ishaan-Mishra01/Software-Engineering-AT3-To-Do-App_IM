#!/usr/bin/env python3
"""
Entry point for To-Do Application
"""
from app import create_app
import os

# Create application instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5001))
    app.run(debug=app.config['DEBUG'], port=port)