#!/usr/bin/python3
"""Module for app_views routing"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    return {"status": "OK"}
