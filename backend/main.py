# ST uses resource-based URIs and HTTP Methods to reduce the complexity of web calls to the API.

#Flask is a lightweight Python web framework (for backend creation)
from flask import Flask, jsonify, request
import json
import route_calculator

# from flask_restful import Api, Resource
#Sqlalchemy is basically a bridge between Py and a SQL DB
#flask-sqlalchemy is an extension for flask that adds sqlalchemy to flas app
# from flask_sqlalchemy import SQLAlchemy
#import urllib.parse
#This is a (Flask library) driver for interacting w PostgreSQL from python
import psycopg2
#os reads from environment
import os

#import cors
from flask_cors import CORS


# #This is to encode the password (in the parameter) for the DB
# urllib.parse.quote_plus("CVkBnjAuwYRIhV3De5hMFxas_HCuQPt_")


#all web requests get sent to this app
#(WSGI) Web Server Gateway Interface is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python
# this creates an instance of flask __name__ is the current running module. 
app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(host='	suleiman.db.elephantsql.com',
                            database='ugcwoeym',
                            user='ugcwoeym',
                            password='vLqVpTJUo53bkUdnoHXr5VdV77nf2m3E')
                            #user=os.environ['DB_USERNAME'],
                            #password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/')
def index():
    return jsonify({"message": "Welcome to SafeWalk!"})

@app.route('/searchRoute', methods=['POST'])
def searchRoute():
    content = request.json

    if content is None:
        return "Failed to search route", 400

    current_location = content['current_location']
    destination = content['destination']

    detailed_route = route_calculator.address_to_route(current_location, destination)

    return jsonify(json.loads(detailed_route))

@app.route('/reportIncident', methods=['GET'])
def create():
    curr = get_db_connection().cursor()
    i=40.7
    j=-75.9
    p=0.000006
    r="hello"
    curr.execute(
        "prepare insert_incident as "
        "INSERT INTO safewalk (latitude, longitude, points, reason)"
         "VALUES ( $1 , $2, $3, $4)")
    curr.execute("insert_incident (%f,%f,%d,%s)",(i,j,p,r))

    return "complete"
    

# This is the maps logic ----------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # this starts server and flask app.
    # debug mode
    app.run(debug=True)