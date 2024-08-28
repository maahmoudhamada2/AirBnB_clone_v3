#!/usr/bin/python3
"""User routing module"""
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Routing method to get users list"""
    usersList = [user.to_dict() for user in storage.all(User).values()]
    return usersList
