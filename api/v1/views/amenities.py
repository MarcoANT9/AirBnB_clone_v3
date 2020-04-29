#!/usr/bin/python3
"""Amenity page for flask that displays class amenities."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ This function retrieves all amenities. Has no parameters. """
    amenities_dict = []
    all_object_dict = storage.all(Amenity).values()
    for value in all_object_dict:
        amenities_dict.append(value.to_dict())
    return jsonify(amenities_dict)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_id_amenity(amenity_id):
    """ This function retrieves one amenity given an id.
        amenity_id → Id of the requested Amenity.
    """
    object_dict = storage.get("Amenity", amenity_id)
    if object_dict:
        return jsonify(object_dict.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_an_amenity(amenity_id):
    """ This function retrieves one amenity given an id and
        deletes it.
        amenity_id → Id of amenity to delete.
        returns an empty dictionary on success.
        raises a 404 error if amenity doesn't exists.
    """
    object_dict = storage.get("Amenity", amenity_id)
    if object_dict:
        object_dict.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenities():
    """ This function creates a new amenity. """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")

    if new_amenity:
        if "name" not in new_amenity:
            abort(400, "Missing name")
        ameni = Amenity(**new_amenity)
        storage.new(ameni)
        storage.save()
        return make_response(jsonify(ameni.to_dict()), 201)


@app_views.route("/amenities/<amenities_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenities_id):
    """ This function updates a amenity. """
    amenity_update = request.get_json()
    if not amenity_update:
        abort(400, "Not a JSON")

    object_ = storage.get("Amenity", amenities_id)
    if object_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in amenity_update.items():
            if key not in ignored_attr:
                setattr(object_, key, value)

            object_.save()
            storage.save()
        return make_response(jsonify(object_.to_dict()), 200)
    abort(404)
