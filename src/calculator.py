import boto3

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

# Print the response
print(route_response)





