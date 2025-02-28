#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.exceptions import *
from models.place import Place


@app_views.route('/cities/<string:place_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_Place_List(place_id):
    """retrieves a list of city objects"""
    try:
        return (jsonify(Place.api_get_all(place_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/cities/<string:place_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(place_id):
    """retrieves a list of city objects or creates new city"""
    try:
        return (jsonify(Place.api_post(
            request.get_json(silent=True),
            place_id)),
            201)
    except BaseModelInvalidObject:
        abort(404)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelMissingAttribute as attr:
        return (jsonify({'error': 'Missing {}'.format(attr)}), 400)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """retrieves, deletes or updates a city object"""
    try:
        return (jsonify(Place.api_get_single(place_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """retrieves, deletes or updates a city object"""
    try:
        return (jsonify(Place.api_delete(place_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_place_by_id(place_id):
    """retrieves, deletes or updates a city object"""
    try:
        return (jsonify(Place.api_put(
                request.get_json(silent=True),
                place_id)), 200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelInvalidObject:
        abort(404)
