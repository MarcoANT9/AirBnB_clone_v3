#!/usr/bin/python3
"""Default RestFul API actions for place's amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_places(place_id):
    list_pl_a = []
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    for place in place.amenities:
        list_pl_a.append(place.to_dict())
    return jsonify(list_pl_a)
