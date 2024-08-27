#!/usr/bin/python3
"""Cities routing"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Routing method to get all cities of a state by its id"""

    key = "{}.{}".format(State.__name__, state_id)

    if key not in storage.all(State):
        abort(404)
    else:
        state = storage.get(State, state_id)
        objsList = [city.to_dict() for city in state.cities]
        return objsList


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'])
def get_city(city_id):
    """Routing method to get a city using id"""
    key = "{}.{}".format(City.__name__, city_id)

    if key not in storage.all(City):
        abort(404)
    if request.method == 'DELETE':
        storage.delete(storage.get(City, city_id))
        storage.save()
        return {}, 200
    else:
        return storage.get(City, city_id).to_dict()
