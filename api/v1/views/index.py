#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns a json of status"""
    return jsonify({"status": "OK"})
