#!/usr/bin/python3
"""Places routing module"""
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views, bodyChecker
from flask import abort, jsonify, request


# ------------------------------------------------------------------------------------


@app_views.route(
    'cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET'])
def get_places(city_id):
    """Routing method to get places of specific city by id"""
    key = "{}.{}".format(City.__name__, city_id)
    if key not in storage.all(City):
        abort(404)
    else:
        city = storage.get(City, city_id)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)


# ------------------------------------------------------------------------------------


@app_views.route(
    '/places/<place_id>',
    strict_slashes=False,
    methods=['GET', 'DELETE'])
def get_place(place_id):
    """Routing method to get place by id"""
    key = "{}.{}".format(Place.__name__, place_id)
    if key not in storage.all(Place):
        abort(404)
    elif request.method == 'DELETE':
        place = storage.get(Place, place_id)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        place = storage.get(Place, place_id)
        return jsonify(place.to_dict())


# ------------------------------------------------------------------------------------
