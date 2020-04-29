#!/usr/bin/python3
"""Default RestFul API actions for cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_all_cities_in_state(state_id):
    """ This function retrieves all the cities in a state one state given an id
        state_id → Id of the requested state.
    """
    all_cities = []
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    all_object_dict = storage.all(City).values()
    for value in all_object_dict:
        if value.state_id == state_id:
            all_cities.append(value.to_dict())
    return jsonify(all_cities)


@app_views.route("cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    """ Retrieves a city given an id.
        city_id → Id of the requested city.
    """
    all_cities = storage.all(City).values()
    for value in all_cities:
        if value.id == city_id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_a_city(city_id):
    """ This function retrieves one city given an id and
        deletes it.
        state_id → Id of state to delete.
        returns an empty dictionary on success.
        raises a 404 error if state doesn't exists.
    """
    city_dict = storage.get(City, city_id)
    print (city_dict)
    if city_dict:
        city_dict.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)

"""
@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    "" This function creates a new state. ""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")

    if new_state:
        if "name" not in new_state:
            abort(400, "Missing name")
        state = State(**new_state)
        storage.new(state)
        storage.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    "" This function updates a state. ""
    state_update = request.get_json()
    if not state_update:
        abort(400, "Not a JSON")

    object_ = storage.get(State, state_id)
    if object_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in state_update.items():
            if key not in ignored_attr:
                setattr(object_, key, value)

            object_.save()
            storage.save()
        return make_response(jsonify(object_.to_dict()), 200)
    abort(404)
"""
