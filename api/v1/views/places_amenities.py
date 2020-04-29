#!/usr/bin/python3
"""Default RestFul API actions for place's amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
