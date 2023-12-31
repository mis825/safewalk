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
CORS(app, origins="*")

def get_db_connection():
    conn = psycopg2.connect(host='suleiman.db.elephantsql.com',
                            database='cbvybryt',
                            user='cbvybryt',
                            password='b_UODoVoWJ4Xzv-TGkfVB33BNsKa63C4')
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

    print("current_location",current_location)
    print("destination",destination)

    detailed_route = route_calculator.calculate_all_routes(current_location, destination)

    return jsonify(json.loads(detailed_route))

@app.route('/calculateAllRoutes', methods=['POST'])
def calculateAllRoutes():
    content = request.json

    if content is None:
        return "Failed to calculate all routes", 400

    current_location = content['current_location']
    destination = content['destination']

    all_routes = route_calculator.calculate_all_routes(current_location, destination)

    return jsonify(json.loads(all_routes))

@app.route('/reportIncident', methods=['GET'])
def create():
    content=request.json
    if content is None:
        return "Failed to search route", 400
    
    conn = get_db_connection()
    curr = conn.cursor()

    content = request.json

    if content is None:
        return "Failed to report incident", 400

    latitude = content['latitude']
    longitude = content['longitude']
    points = content['points']
    reason = content['reason']

    # We may not allow user to write the reasoning due to safety concerns
    curr.execute(
        "prepare insert_incident as "
        "INSERT INTO safewalk (latitude, longitude, points, reason)"
         "VALUES ($1,$2,$3,$4)")
    curr.execute("execute insert_incident (%s,%s,%s,%s)", (
        latitude,
        longitude,
        points,
        reason
    ))
    conn.commit()
    curr.close()
    conn.close()

    return "Incident reported!"

@app.route('/getIncidents', methods=['GET'])
def getIncidents():
    conn = get_db_connection()
    curr = conn.cursor()

    # We may not allow user to write the reasoning due to safety concerns
    curr.execute(
        "SELECT * FROM safewalk"
    )

    rows = curr.fetchall()

    incidents = []
    for row in rows:
        incident = { # latitude, longitude, points, reason
            'latitude': row[0],
            'longitude': row[1],
            'points': row[2],
            'reason': row[3]
        }
        incidents.append(incident)

    curr.close()
    conn.close()

    return jsonify({'incidents': incidents})

# This is the maps logic ----------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # this starts server and flask app.
    # debug mode
    app.run(debug=True)