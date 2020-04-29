#!/usr/bin/python3
"""Default RestFul API actions for cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def get_one_state(state_id):
    """ This function retrieves one state given an id.
        state_id → Id of the requested state.
    """
    object_dict = storage.get("State", state_id)
    if object_dict:
        return jsonify(object_dict.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_an_state(state_id):
    """ This function retrieves one state given an id and
        deletes it.
        state_id → Id of state to delete.
        returns an empty dictionary on success.
        raises a 404 error if state doesn't exists.
    """
    object_dict = storage.get("State", state_id)
    if object_dict:
        object_dict.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """ This function creates a new state. """
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
    """ This function updates a state. """
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
