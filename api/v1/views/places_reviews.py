#!/usr/bin/python3
"""Default RestFul API actions for place's reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_in_place(place_id):
    """ This function retrieves all the reviews in a place given a place id
        place_id → Id of the requested place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review_list = [r.to_dict() for r in place.reviews]
    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_id_review(review_id):
    """ Retrieves a review given an id.
        review_id → Id of the requested review.
    """
    review_dict = storage.get(Review, review_id)
    if review_dict is None:
        abort(404)
    return jsonify(review_dict.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """ This function retrieves one review given an id and
        deletes it.
        review_id → Id of review to delete.
        returns an empty dictionary on success.
        raises a 404 error if state doesn't exists.
    """
    review_dict = storage.get(Review, review_id)
    if review_dict:
        review_dict.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ This function creates a new review.
        place_id → Place in which the new review will be created.
    """
    new_review = request.get_json()
    if new_review is None:
        abort(400, "Not a JSON")
    if not new_review.get("text"):
        abort(400, "Missing text")
    if not new_review.get("user_id"):
        abort(400, "Missing user_id")

    place = storage.get("Place", place_id)
    if not storage.get("User", new_review.get("user_id")):
        abort(404)

    if not place:
        abort(404)

        review = Review(**new_review)
        storage.new(review)
        setattr(review, "place_id", place_id)
        storage.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ This function updates a review given an id.
        review_id → id of the review to update.
    """
    review_update = request.get_json()
    if review_update is None:
        abort(400, "Not a JSON")

    object_ = storage.get(Review, review_id)
    if object_:
        ignored_atr = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in review_update.items():
            if key not in ignored_atr:
                setattr(object_, key, value)
            object_.save()
            storage.save()
        return make_response(jsonify(object_.to_dict()), 200)
    abort(404)
