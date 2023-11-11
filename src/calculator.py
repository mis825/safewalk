import boto3

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

# Function to print a detailed description of the route in feet
# Function to print a detailed description of the route in feet with swapped coordinates in the print
def describe_route(route_response):
    print("Route Description:")
    for leg in route_response.get('Legs', []):
        for step in leg.get('Steps', []):
            # Convert meters to feet (1 meter = 3.28084 feet)
            distance_in_feet = step['Distance'] * 3.28084 * 1000
            # Format distance as a string with two decimal places
            distance_text = "{:.2f} feet".format(distance_in_feet)
            # Swap latitude and longitude in the print statement
            instruction = "From {} to {}".format(
                (step['StartPosition'][1], step['StartPosition'][0]),  # Swap latitude and longitude
                (step['EndPosition'][1], step['EndPosition'][0])          # Swap latitude and longitude
            )
            print(distance_text + ": " + instruction)

# Print the detailed route description in feet with swapped coordinates in the print
describe_route(route_response)
