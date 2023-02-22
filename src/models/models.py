from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

class User(db.Model, UserMixin):
    """Stores the user's details."""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(100))

    saved_job = db.relationship('Saved')

    
class Saved(db.Model, UserMixin):
    """Stores the user's saved jobs."""
    
    id = db.Column(db.Integer(), primary_key=True)
    job_title = db.Column(db.String(500))
    description = db.Column(db.String())
    link= db.Column(db.String())
    applied_to = db.Column(db.Boolean())
    closing_date = db.Column(db.Date())
    
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
