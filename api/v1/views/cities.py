#!/usr/bin/python3

""" New view for City objects to handle default RESTful API actions """

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):

    """ Retrieve all City objects of a State """

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):

    """ Retrieve a City object by ID """

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):

    """ Delete a City object by ID """

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):

    """ Create a new City object """

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    
    new_city = City(name=data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):

    """ Update an existing City object """

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    
    storage.save()
    return jsonify(city.to_dict()), 200
