# App Directory

This directory contains the Flask application code for the To-Do app.

## Structure

- `__init__.py` - Application factory and initialization
- `config.py` - Configuration settings for different environments
- `routes.py` - URL routes and view functions
- `models.py` - Data models and storage functions

## Application Factory Pattern

The app uses the Flask application factory pattern for better testing and configuration management:

```python
from app import create_app

app = create_app('development')
```

## Configuration

Configuration is managed through environment-specific classes:
- `DevelopmentConfig` - For local development
- `TestingConfig` - For running tests
- `ProductionConfig` - For production deployment

## Blueprints

Routes are organized using Flask blueprints. All routes are registered under the `main` blueprint.