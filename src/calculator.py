import boto3
import json
# Initialize the AWS Location Service client
client = boto3.client('location', region_name='us-east-2')

place_index = 'SafeWalk'
calculator_name = 'SafeWalk'

# Specify the start and end addresses
start_address = '405 Selfridge StBethlehem, PA 18015'
end_address = '201 E Packer Ave, Bethlehem, PA 18015'

# Function to geocode an address and return latitude and longitude separately
def geocode_address(client, place_index, address):
    response = client.search_place_index_for_text(IndexName=place_index, Text=address)
    result = response['Results'][0]
    latitude = result['Place']['Geometry']['Point'][1]
    longitude = result['Place']['Geometry']['Point'][0]
    return latitude, longitude

# Geocode the start and end addresses
start_latitude, start_longitude = geocode_address(client, place_index, start_address)
end_latitude, end_longitude = geocode_address(client, place_index, end_address)

# Make the API call to calculate the route
route_response = client.calculate_route(
    CalculatorName=calculator_name,
    DeparturePosition=[start_longitude, start_latitude],
    DestinationPosition=[end_longitude, end_latitude],
    TravelMode='Walking'  
)
print("Start Latitude:", start_latitude)
print("Start Longitude:", start_longitude)
print("End Latitude:", end_latitude)
print("End Longitude:", end_longitude)

# Function to return a JSON object with the specified format
def describe_route(route_response):
    route_description = {"points": []}
    point_index = 0  # Initialize the point index
    
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
            route_description["points"].append((str(point_index), point))
            point_index += 1  # Increment the point index

    return json.dumps(route_description, indent=2)

# Get the detailed route description in the specified JSON format
detailed_route = describe_route(route_response)
print(detailed_route)