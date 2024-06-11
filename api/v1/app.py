#!/usr/bin/python3

""" This module initializes and runs a Flask web server"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

# Initialize Flask application
app = Flask(__name__)

app.register_blueprint(app_views)

app.url_map.strict_slashes = False

@app.teardown_appcontext
def downtear(self):

    """ Close the storage session """

    storage.close()

@app.errorhandler(404)
def page_not_found(error):

    """ This function returns a JSON response with a
    404 status code when a page is not found."""

    return jsonify(error='Not found'), 404

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    
    # Run the Flask application
    app.run(host=host, port=port, threaded=True)
