#!/usr/bin/python3
"""Main app for AirBnB_clone site"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


@app.teardown_appcontext
def resetDB(self):
    """Method to reset Databases"""
    storage.close()


app.register_blueprint(app_views)


if __name__ == '__main__':
    hst = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else '0.0.0.0'
    prt = int(getenv("HBNB_API_PORT")) if getenv("HBNB_API_PORT") else 5000
    app.run(host=hst, port=prt, threaded=True)
