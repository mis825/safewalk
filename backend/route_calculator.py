import boto3
import json
import os

# Start boto3 client
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
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
