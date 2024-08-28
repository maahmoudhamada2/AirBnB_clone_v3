#!/usr/bin/python3
"""Amenities module"""
from api.v1.views import app_views, bodyChecker
from models.amenity import Amenity
from models import storage
from flask import request, abort


# --------------------------------------------------------------------------------------------


@app_views.route(
    '/amenities',
    strict_slashes=False,
    methods=['GET', 'POST'])
def get_amenities():
    """Routing method to get list of amenities"""
    objs = storage.all(Amenity)
    if request.method == 'POST':
        mssg = bodyChecker(request.method)
        if mssg:
            return mssg, 400
        else:
            amenity = Amenity()
            for key, value in request.get_json().items():
                setattr(amenity, key, value)
            amenity.save()
            return amenity.to_dict(), 201
    else:
        amenities = [amenity.to_dict() for amenity in objs.values()]
        return amenities

# --------------------------------------------------------------------------------------------


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['GET', 'DELETE', 'PUT'])
def get_amenity(amenity_id):
    """Routing method to get an amenity by id"""

    key = "{}.{}".format(Amenity.__name__, amenity_id)
    skipKeys = ['id', 'created_at', 'updated_at']

    if key not in storage.all(Amenity):
        abort(404)
    elif request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)
        storage.delete(amenity)
        storage.save()
        return {}, 200
    elif request.method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        for key, value in request.get_json().items():
            if key in skipKeys:
                continue
            else:
                setattr(amenity, key, value)
        amenity.save()
        return amenity.to_dict(), 200
    else:
        return storage.get(Amenity, amenity_id).to_dict()
