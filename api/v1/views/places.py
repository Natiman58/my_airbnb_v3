#!/usr/bin/python3
"""
    A module for handeling RESTFul API actions for Place object
    GET DELETE PUT POST
"""
from flask import request, abort, jsonify
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models import storage

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city_id(city_id):
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    return jsonify([place.to_dict() for place in cities.places]), 200

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_by_place_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_places_by_place_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_places_by_city_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'Missing user_id'}), 400
    if 'name' not in data:
        return jsonify({'Missing name'}), 400

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data['user_id'] = user_id
    data['city_id'] = city_id
    place = Place(**data)

    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_by_place_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({'Not a JSON'}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
