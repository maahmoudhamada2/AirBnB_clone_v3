#!/usr/bin/python3
"""User routing module"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request

# -------------------------------------------------------------------------


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Routing method to get users list"""
    usersList = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(usersList)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Routing method to get a user by id"""
    key = "{}.{}".format(User.__name__, user_id)
    if key not in storage.all(User):
        abort(404)
    else:
        user = storage.get(User, user_id)
        return jsonify(user.to_dict())
