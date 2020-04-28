#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns a json of status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def storage_numbers():
    """Return the numbers of all classes in storage"""
    cls_numbers = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_numbers)
