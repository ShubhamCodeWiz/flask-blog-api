from flask import Blueprint, Flask, jsonify, request
from marshmallow import ValidationError

users_bp = Blueprint("users", __name__)

from ..schemas import UserSchema
from ..models import User
from .. import db

# instantiate Userschema obj
user_schema = UserSchema()

#POST: create a user
@users_bp.route("/users", methods=['POST'])
def create_user():
    user_data = request.get_json()
    # Check if username and password are provided
    if 'username' not in user_data or 'password' not in user_data:
        return jsonify({"error": "username and password are required"}), 400

    new_user = User(username=user_data['username'])
    new_user.set_password(user_data['password']) # Hash the password
    
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201


