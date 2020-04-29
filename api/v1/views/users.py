#!/usr/bin/python3
"""User page for flask that displays class user."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_users():
    """ This function retrieves all users. Has no parameters. """
    users_dict = []
    all_object_dict = storage.all(User).values()
    for value in all_object_dict:
        users_dict.append(value.to_dict())
    return jsonify(users_dict)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_id_user(user_id):
    """ This function retrieves one user given an id.
        user_id → Id of the requested User.
    """
    object_dict = storage.get("User", user_id)
    if object_dict:
        return jsonify(object_dict.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_an_user(user_id):
    """ This function retrieves one user given an id and
        deletes it.
        user_id → Id of user to delete.
        returns an empty dictionary on success.
        raises a 404 error if user doesn't exists.
    """
    object_dict = storage.get("User", user_id)
    if object_dict:
        object_dict.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def create_user():
    """ This function creates a new user. """
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")

    if not new_user.get("email"):
        abort(400, "Missing email")

    if not new_user.get("password"):
        abort(400, "Missing password")

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ This function updates a user. """
    user_update = request.get_json()
    if not user_update:
        abort(400, "Not a JSON")

    object_ = storage.get("User", user_id)
    if object_:
        ignored_attr = ["id", "created_at", "updated_at"]
        for key, value in user_update.items():
            if key not in ignored_attr:
                setattr(object_, key, value)

            object_.save()
            storage.save()
        return make_response(jsonify(object_.to_dict()), 200)
    abort(404)
