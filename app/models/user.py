import datetime

from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    created_at = db.Column(db.Integer, unique=False, nullable=False)
    updated_at = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

        timestamp = int(datetime.datetime.utcnow().timestamp())
        self.created_at = timestamp
        self.updated_at = timestamp

    def __repr__(self):
        return f'<User {self.email}>'
