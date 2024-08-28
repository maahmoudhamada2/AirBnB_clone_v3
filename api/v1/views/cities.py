#!/usr/bin/python3
"""Cities routing"""
from api.v1.views import app_views, bodyChecker
from models.state import State
from models.city import City
from models import storage
from flask import abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_cities(state_id):
    """Routing method to get all cities of a state by its id"""

    key = "{}.{}".format(State.__name__, state_id)

    if key not in storage.all(State):
        abort(404)
    if request.method == 'POST':
        mssg = bodyChecker(request.method)
        if mssg:
            return mssg, 400
        else:
            city = City()
            setattr(city, 'state_id', state_id)
            for key, value in request.get_json().items():
                setattr(city, key, value)
            city.save()
            return city.to_dict(), 201
    else:
        state = storage.get(State, state_id)
        objsList = [city.to_dict() for city in state.cities]
        return objsList


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_city(city_id):
    """Routing method to get a city using id"""

    key = "{}.{}".format(City.__name__, city_id)
    skipKeys = ['id', 'state_id', 'updated_at', 'created_at']

    if key not in storage.all(City):
        abort(404)
    if request.method == 'DELETE':
        storage.delete(storage.get(City, city_id))
        storage.save()
        return {}, 200
    elif request.method == 'PUT':
        mssg = bodyChecker(request.method)
        if mssg:
            return mssg, 400
        else:
            city = storage.get(City, city_id)
            for key, value in request.get_json().items():
                if key in skipKeys:
                    continue
                else:
                    setattr(city, key, value)
            city.save()
            return city.to_dict(), 200
    else:
        return storage.get(City, city_id).to_dict()
