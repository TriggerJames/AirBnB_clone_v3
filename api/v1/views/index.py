#!/usr/bin/python3

""" Module to define API status endpoints """

import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    
    """Return API status as JSON"""
    
    return jsonify(status='OK')

@app_views.route('/stats', strict_slashes=False)
def stuff():

    """ Return counts of different object types in JSON format """

    todos = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }
    
    # Count the number of each type of object and store in dictionary
    for key in todos:
        todos[key] = storage.count(todos[key])
        
    # Return the counts
    return jsonify(todos)
