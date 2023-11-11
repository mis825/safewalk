# ST uses resource-based URIs and HTTP Methods to reduce the complexity of web calls to the API.

#Flask is a lightweight Python web framework (for backend creation)
from flask import Flask, jsonify, request
import boto3

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

# Start boto3 client
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
place_index = 'SafeWalk'  
calculator_name = 'SafeWalk'

client = boto3.client('location', region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

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

    # start_latitude, start_longitude = geocode_address(client, place_index, start_address)

    # data = {
    #     "start_lattitude": start_latitude,
    #     "start_longitude": start_longitude
    # }
    
    return jsonify({"message": "Welcome to SafeWalk!"})

@app.route('/searchRoute', methods=['POST'])
def searchRoute():
    content = request.json

    if content is None:
        return "Failed to search route", 400

    current_location = content['current_location']
    destination = content['destination']

    start_latitude, start_longitude = geocode_address(client, place_index, current_location)
    end_latitude, end_longitude = geocode_address(client, place_index, destination)

    start_end_coordinates = {
        "start_latitude": start_latitude,
        "start_longitude": start_longitude,
        "end_latitude": end_latitude,
        "end_longitude": end_longitude
    }

    return jsonify(start_end_coordinates);

# This is the maps logic ----------------------------------------------------------------------------

# Function to geocode an address
def geocode_address(client, place_index, address):
    response = client.search_place_index_for_text(IndexName=place_index, Text=address)
    result = response['Results'][0]
    latitude = result['Place']['Geometry']['Point'][1]
    longitude = result['Place']['Geometry']['Point'][0]
    return latitude, longitude
# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # this starts server and flask app.
    # debug mode
    app.run(debug=True)