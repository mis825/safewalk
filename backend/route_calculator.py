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

place_index = 'SafeWalk'  
calculator_name = 'SafeWalk'

client = boto3.client('location', region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Function to geocode an address
def geocode_address(address):
    response = client.search_place_index_for_text(IndexName=place_index, Text=address)
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

    # First loop to find the route with the least points and calculate points for each route
    route_points = []
    for index, route in enumerate(directions_result):
        points = calculate_points_for_route(route, incidents_data)
        route_points.append(points)  # Store points for each route

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
            "total_points": route_points[index],  # Include total points for the route
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
    print(route_info)

    return routes_json_output

def calculate_points_for_route(route, incidents_data):
    points = 0
    proximity_threshold = 0.0005  # Define a threshold for proximity

    for step in route["legs"][0]["steps"]:
        # Calculate the bounding box for the step with a proximity buffer
        min_lat = min(step["start_location"]["lat"], step["end_location"]["lat"]) - proximity_threshold
        max_lat = max(step["start_location"]["lat"], step["end_location"]["lat"]) + proximity_threshold
        min_lng = min(step["start_location"]["lng"], step["end_location"]["lng"]) - proximity_threshold
        max_lng = max(step["start_location"]["lng"], step["end_location"]["lng"]) + proximity_threshold

        for incident in incidents_data['incidents']:
            incident_lat = incident['latitude']
            incident_lng = incident['longitude']

            # Check if the incident is within or close to the bounding box
            if min_lat <= incident_lat <= max_lat and min_lng <= incident_lng <= max_lng:
                points += incident['points'] * 10000
                print(incident_lat,incident_lng)
    return points

def is_close(location, incident_location):
    """
    Check if the location is within 0.001 degrees of latitude and longitude
    from the incident location.
    """
    lat_close = abs(location['lat'] - incident_location[0]) <= 0.0004
    lng_close = abs(location['lng'] - incident_location[1]) <= 0.00004
    return lat_close and lng_close
