#!/usr/bin/python3
"""Create an instace blueprint"""
from flask import Blueprint

app_views = Blueprint("my_blueprint", __name__, url_prefix="/api/v1")

"""Import flask views"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
