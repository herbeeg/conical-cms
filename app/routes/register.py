from flask import Blueprint, jsonify, request

registration = Blueprint('registration', __name__)

@registration.route('/register', methods=['POST'])
def register():
    error = None

    if 'POST' == request.method:
        message = 'Registration successful.'

        return jsonify({
            'message': message
        }), 200
