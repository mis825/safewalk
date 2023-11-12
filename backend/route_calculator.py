import boto3
import json
import os
import heapq
import random
import googlemaps
from main import getIncidents


# Start boto3 client
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)

print('acc key:', access_key)
print('sec key:', secret_key)
print('api key:', api_key)

place_index = 'SafeWalk'  
calculator_name = 'SafeWalk'

print('hi!)')
client = boto3.client('location', region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
print('bye!)')
# Function to geocode an address
def geocode_address(address):
    print('hiiiiii')
    response = client.search_place_index_for_text(IndexName=place_index, Text=address)
    print('cant catch me')
    result = response['Results'][0]
    latitude = result['Place']['Geometry']['Point'][1]
    longitude = result['Place']['Geometry']['Point'][0]
    return latitude, longitude

def describe_route(route_response):
    route_description = {"points": []}
    
    for leg in route_response.get('Legs', []):
        for step in leg.get('Steps', []):
            # Convert meters to feet (1 meter = 3.28084 feet)
            distance_in_feet = step['Distance'] * 3.28084 * 1000
            # Format distance as a string with two decimal places
            distance_text = "{:.2f} feet".format(distance_in_feet)
            
            # Extract coordinates
            from_lat, from_lon = step['StartPosition'][1], step['StartPosition'][0]
            to_lat, to_lon = step['EndPosition'][1], step['EndPosition'][0]

            # Create a dictionary for the point
            point = {
                "distance": distance_text,
                "from_lat": from_lat,
                "from_lon": from_lon,
                "to_lat": to_lat,
                "to_lon": to_lon
            }
            
            # Add the point to the array with the current index
            route_description["points"].append(point)

    return json.dumps(route_description)

def address_to_route(current_location, destination):
    start_latitude, start_longitude = geocode_address(current_location)
    end_latitude, end_longitude = geocode_address(destination)

    route_response = client.calculate_route(
    CalculatorName=calculator_name,
    DeparturePosition=[start_longitude, start_latitude],
    DestinationPosition=[end_longitude, end_latitude],
    TravelMode='Walking'  
    )

    return describe_route(route_response)


def calculate_all_routes(current_location, destination):
    # Request walking directions
    directions_result = gmaps.directions(current_location, destination, mode="walking", alternatives=True)

    routes_info = []
    min_points = float('inf')  # Initialize with a very high number
    best_route_index = None
    incidents_response = getIncidents()
    incidents_data = incidents_response.get_json()  # Extract JSON data from the response

    # First loop to find the route with the least points
    for index, route in enumerate(directions_result):
        points = calculate_points_for_route(route,incidents_data)  
        if points < min_points:
            min_points = points
            best_route_index = index

    # Second loop to process routes and set 'is_best'
    for index, route in enumerate(directions_result):
        route_info = {
            "index": index,
            "summary": route["summary"],
            "distance": route["legs"][0]["distance"]["text"],
            "duration": route["legs"][0]["duration"]["text"],
            "is_best": index == best_route_index,  # Set 'is_best' only for the best route
            "steps": [{
                "instruction": step["html_instructions"],
                "distance": step["distance"]["text"],
                "duration": step["duration"]["text"],
                "start_location": {
                    "lat": step["start_location"]["lat"],
                    "lng": step["start_location"]["lng"]
                },
                "end_location": {
                    "lat": step["end_location"]["lat"],
                    "lng": step["end_location"]["lng"]
                }
            } for step in route["legs"][0]["steps"]]
        }
        routes_info.append(route_info)

    # Create dictionary for routes
    routes_data = {"routes": routes_info}

    # Convert to JSON
    routes_json_output = json.dumps(routes_data, indent=4)
    print(routes_info)

    return routes_json_output

def calculate_points_for_route(route,incidents_data):
    # Call getIncidents to retrieve incident data
    

    points = 0

    for step in route["legs"][0]["steps"]:
        start_location = step["start_location"]
        end_location = step["end_location"]

        for incident in incidents_data['incidents']:
            incident_location = (incident['latitude'], incident['longitude'])

            # Check if the incident is close to the start or end location of the step
            if is_close(start_location, incident_location) or is_close(end_location, incident_location):
                points += incident['points']  

    return points

def is_close(location, incident_location):
    """
    Check if the location is within 0.001 degrees of latitude and longitude
    from the incident location.
    """
    lat_close = abs(location['lat'] - incident_location[0]) <= 0.001
    lng_close = abs(location['lng'] - incident_location[1]) <= 0.001
    return lat_close and lng_close
