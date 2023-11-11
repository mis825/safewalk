import boto3

# Initialize the AWS Location Service client
client = boto3.client('location', region_name='us-east-2')

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
start_latitude, start_longitude = geocode_address(client, place_index, start_address)
end_latitude, end_longitude = geocode_address(client, place_index, end_address)


# Make the API call to calculate the route
route_response = client.calculate_route(
    CalculatorName=calculator_name,
    DeparturePosition=[start_longitude, start_latitude],
    DestinationPosition=[end_longitude, end_latitude],
    TravelMode='Walking'  
)

# Debugging: Print the raw route response
print("Raw Route Response:")
print(route_response)

# Function to print a detailed description of the route
def describe_route(route_response):
    print("Route Description:")
    for leg in route_response.get('Legs', []):
        for step in leg.get('Steps', []):
            # Format distance as a string with two decimal places
            distance_text = "{:.2f} meters".format(step['Distance'] * 1000)  # Assuming distance is in kilometers
            # The instruction is not provided in the response, so we use start and end positions
            instruction = "From {} to {}".format(step['StartPosition'], step['EndPosition'])
            print(distance_text + ": " + instruction)

# Print the detailed route description
describe_route(route_response)

