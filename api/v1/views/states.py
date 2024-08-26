#!/usr/bin/python3
"""States routing"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/states', methods=['GET'])
def get_states():
    """Routing method to list states objs"""
    objs, objList = storage.all(State), []
    for obj in objs.values():
        objList.append(obj.to_dict())
    return jsonify(objList)


@app_views.route('/states/<state_id>')
def single_state(state_id):
    """Routing method to get single state by id"""
    objs = storage.all(State)
    key = "{}.{}".format(State.__name__, state_id)
    if key not in objs:
        abort(404)
    else:
        return jsonify(objs.get(key).to_dict())
