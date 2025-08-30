# src/auth/routes.py
from flask import Blueprint, jsonify, request
from ..models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401