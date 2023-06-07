#!/usr/bin/python3
"""
    package that contains the necessary routes and logic for your API endpoints.
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """
        api endpoint /status to get the status of api
    """
    return jsonify({"status": "OK"})
