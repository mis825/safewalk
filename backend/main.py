# ST uses resource-based URIs and HTTP Methods to reduce the complexity of web calls to the API.

#Flask is a lightweight Python web framework (for backend creation)
from flask import Flask, jsonify
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

    start_latitude, start_longitude = geocode_address(client, place_index, start_address)

    data = {
        "start_lattitude": start_latitude,
        "start_longitude": start_longitude
    }
    
    return jsonify(data)

access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

client = boto3.client('location', region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

place_index = 'SafeWalk'  
calculator_name = 'SafeWalk' 

# Specify the start and end addresses
start_address = '405 Selfridge StBethlehem, PA 18015'  
end_address = '201 E Packer Ave, Bethlehem, PA 18015'  

# Function to geocode an address
def geocode_address(client, place_index, address):
    response = client.search_place_index_for_text(IndexName=place_index, Text=address)
    result = response['Results'][0]
    latitude = result['Place']['Geometry']['Point'][1]
    longitude = result['Place']['Geometry']['Point'][0]
    return latitude, longitude

# Geocode the start and end addresses
# end_latitude, end_longitude = geocode_address(client, place_index, end_address)



# Make the API call to calculate the route
# route_response = client.calculate_route(
#     CalculatorName=calculator_name,
#     DeparturePosition=[start_longitude, start_latitude],
#     DestinationPosition=[end_longitude, end_latitude],
#     TravelMode='Walking'  
# )

# Print the response
# print(route_response)

if __name__ == "__main__":
    # this starts server and flask app.
    # debug mode
    app.run(debug=True)