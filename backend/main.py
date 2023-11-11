# ST uses resource-based URIs and HTTP Methods to reduce the complexity of web calls to the API.

#Flask is a lightweight Python web framework (for backend creation)
from flask import Flask

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
    return "helloworld!"


if __name__ == "__main__":
    # this starts server and flask app.
    # debug mode
    app.run(debug=True)