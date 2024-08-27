#!/usr/bin/python3
"""States routing"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, request, jsonify


def bodyChecker(method):
    if method == 'POST':
        if not request.is_json:
            return 'Not a JSON'
        if not request.get_json() or not isinstance(request.get_json(), dict):
            return 'Not a JSON'
        elif 'name' not in request.get_json():
            return 'Missing name'
        else:
            return None
    else:
        if not request.is_json:
            return 'Not a Json'
        if not request.get_json() or not isinstance(request.get_json(), dict):
            return 'Not a JSON'
        else:
            return None

# -------------------------------------------------------------------------------


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def get_states():
    """Routing method to list states objs"""

    objs, objList = storage.all(State), []

    if request.method == 'POST':
        mssg = bodyChecker(request.method)
        if mssg:
            return mssg, 400
        else:
            s = State()
            for key, value in request.get_json().items():
                setattr(s, key, value)
            s.save()
            return s.to_dict(), 201
    else:
        for obj in objs.values():
            objList.append(obj.to_dict())
        return objList

# -------------------------------------------------------------------------------


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def single_state(state_id):
    """Routing method to get single state by id"""

    objs = storage.all(State)
    key = "{}.{}".format(State.__name__, state_id)
    skipKeys = ['id', 'created_at', 'updated_at']

    if key not in objs:
        abort(404)

    elif request.method == 'DELETE':
        storage.delete(objs.get(key))
        storage.save()
        return {}, 200

    elif request.method == 'PUT':
        mssg = bodyChecker(request.method)
        if mssg:
            return mssg, 400
        else:
            obj = objs.get(key)
            for key, value in request.get_json().items():
                if key in skipKeys:
                    continue
                else:
                    setattr(obj, key, value)
            obj.save()
            return obj.to_dict(), 200
    else:
        return objs.get(key).to_dict()
