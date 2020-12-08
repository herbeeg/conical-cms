from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from app.database import db
from app.models.user import User

registration = Blueprint('registration', __name__)

@registration.route('/register', methods=['POST'])
def register():
    error = None

    if 'POST' == request.method:
        duplicates = db.session.query(
            User
        ).filter(
            (request.json['email'] == User.email) | 
            (request.json['username'] == User.username)
        ).all()

        if duplicates:
            error = 'A user with that email address or username already exists.'
        else:
            new_user = User(
                request.json['email'],
                request.json['username'],
                generate_password_hash(request.json['password'])
            )
            db.session.add(new_user)
            db.session.commit()

            message = 'Registration successful.'

            return jsonify({
                'message': message
            }), 200

        return jsonify({
            'message': error
        }), 400
