"""
To-Do Application Package
"""
from flask import Flask
from app.config import config
from app.databases import db
import os

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])

    db.init_app(app) #initalise db
    from app import databases #so that User and Task can be loaded
    
    # Register blueprints/routes
    from app.routes import main, calendar_routes
    app.register_blueprint(main)
    app.register_blueprint(calendar_routes)
    
    return app