#!/usr/bin/python3
"""Module for app_views routing"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """Method to show stat of objs"""
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review
    from models.place import Place
    from models.user import User
    from models import storage

    obj_stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return obj_stats
