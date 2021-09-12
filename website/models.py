from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    paste = db.relationship('Paste')

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, timezone=True, default=func.now(), nullable=False)