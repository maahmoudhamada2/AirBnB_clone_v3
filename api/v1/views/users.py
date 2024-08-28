#!/usr/bin/python3
"""User routing module"""
from models.user import User
from models import storage
from api.v1.views import app_views, bodyChecker
from flask import jsonify, abort, request

# -------------------------------------------------------------------------


def advBodyChecker():
    if not request.is_json:
        return "Not a JSON"
    elif not request.get_json():
        return "Not a JSON"
    elif 'email' not in request.get_json():
        return "Missing email"
    elif 'password' not in request.get_json():
        return "Missing password"
    else:
        return None


# -------------------------------------------------------------------------


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def get_users():
    """Routing method to get users list"""
    if request.method == 'POST':
        mssg = advBodyChecker()
        if mssg:
            return jsonify(mssg), 400
        else:
            user = User()
            for key, value in request.get_json().items():
                setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 201
    else:
        usersList = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(usersList)


# -------------------------------------------------------------------------


@app_views.route(
    '/users/<user_id>',
    strict_slashes=False,
    methods=['GET', 'DELETE', 'PUT'])
def get_user(user_id):
    """Routing method to get a user by id"""

    key = "{}.{}".format(User.__name__, user_id)
    skipKeys = ['id', 'email', 'created_at', 'updated_at']

    if key not in storage.all(User):
        abort(404)
    elif request.method == 'DELETE':
        user = storage.get(User, user_id)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        mssg = bodyChecker(request.method)
        if mssg:
            return jsonify(mssg), 400
        else:
            user = storage.get(User, user_id)
            for key, value in request.get_json().items():
                if key in skipKeys:
                    continue
                else:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200
    else:
        user = storage.get(User, user_id)
        return jsonify(user.to_dict())


# -------------------------------------------------------------------------
