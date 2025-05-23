from flask_sqlalchemy import SQLAlchemy


#Keep in mind this is a work in progress build.

db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False) #need to make it so it stores as hashed.

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password


#similar to edstem stuff:
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    priority = db.Column(db.Integer, default=0)
    is_complete = db.Column(db.Boolean, default=False)

    def __init__(self, title, description=None, priority=0):
        self.title = title
        self.description = description
        self.priority = priority
        self.is_complete = False