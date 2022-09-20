#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.expections import *
from models.state import State


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    return (jsonify(State.api_get_all()), 200)

@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False)
def post_a_state():
    """Creates a State"""
    try:
        returnedValue = State.api_post(
                    request.get_json(silent=True))
        return (jsonify(returnedValue), 200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': 'Not a JSON'}), 400)
    except BaseModelMissingAttribute as e:
        return (jsonify({'error': 'Missing {}'.
                        format(e)}), 400)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """handles State object: state_id"""
    try:
        returnedValue = State.api_get_single(state_id)
        return (jsonify(returnedValue), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def del_state_by_id(state_id):
    """handles PUT State object: state_id"""
    try:
        return (jsonify(State.api_delete(state_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_state_by_id(state_id):
    """handles PUT State object: state_id"""
    try:
        returnedValue= State.api_put(
                        request.get_json(silent=True),
                        storage.get("State", state_id))
        storage.save()
        return (jsonify(returnedValue), 200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': 'Not a JSON'}), 400)
    except BaseModelInvalidObject:
        abort(404)