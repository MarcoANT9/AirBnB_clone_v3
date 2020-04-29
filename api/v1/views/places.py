#!/usr/bin/python3
"""Place page for flask that displays class places."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    """ This function retrieves places in cities. """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_list = [p.to_dict() for p in city.places]
    return jsonify(places_list), 200


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_id_place(place_id):
    """ This function retrieves one place given an id.
        place_id → Id of the requested Place.
    """
    object_dict = storage.get("Place", place_id)
    if object_dict:
        return jsonify(object_dict.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ This function retrieves one place given an id and
        deletes it.
        place_id → Id of places to delete.
        returns an empty dictionary on success.
        raises a 404 error if place doesn't exists.
    """
    object_dict = storage.get("Place", place_id)
    if object_dict:
        object_dict.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ This function creates a new place. """
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if not new_place.get("name"):
        abort(400, "Missing name")
    if not new_place.get("user_id"):
        abort(400, "Missing user_id")

    city = storage.get("City", city_id)
    if not storage.get("User", new_place.get("user_id")):
        abort(404)

    if not city:
        abort(404)

    pla = Place(**new_place)
    setattr(pla, "city_id", city_id)
    storage.new(pla)
    storage.save()
    return make_response(jsonify(pla.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_places(place_id):
    """ This function updates a place. """
    place_update = request.get_json()
    if not place_update:
        abort(400, "Not a JSON")

    object_ = storage.get("Place", place_id)
    if object_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in place_update.items():
            if key not in ignored_attr:
                setattr(object_, key, value)

            object_.save()
            storage.save()
        return make_response(jsonify(object_.to_dict()), 200)
    abort(404)
