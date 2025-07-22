from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

def cleanup_old_completed_tasks(user_email, days_old=30):
    cutoff = datetime.now() - timedelta(days=days_old)
    old_tasks = Task.query.filter_by(user_email=user_email, completed=True).filter(Task.completed_date < cutoff).all()
    count = len(old_tasks)

    for task in old_tasks:
        db.session.delete(task)
    db.session.commit()
    return count

class User(db.Model):
    __tablename__ = 'users'
    
    email = db.Column(db.String(120), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    priority = db.Column(db.Integer, default=0)
    is_complete = db.Column(db.Boolean, default=False)
    list = db.Column(db.String(50), default='All Tasks')
    due_date = db.Column(db.String(20), nullable=True)
    created = db.Column(db.DateTime, nullable=False)
    completed_date = db.Column(db.DateTime, nullable=True)

    user_email = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)

    def __init__(self, title, description=None, priority=0):
        self.title = title
        self.description = description
        self.priority = priority
        self.is_complete = False

