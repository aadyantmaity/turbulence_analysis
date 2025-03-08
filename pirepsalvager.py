import math

def calculate_new_coordinates(input_str):
    
    lat1 = 33.9416
    lon1 = -118.4085
    
    degrees = int(input_str[:3])
    nautical_miles = int(input_str[3:])
    
    distance_km = nautical_miles * 1.852
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    
    bearing = math.radians(degrees)
    
    lat2 = math.asin(math.sin(lat1) * math.cos(distance_km / 6371) +
                     math.cos(lat1) * math.sin(distance_km / 6371) * math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance_km / 6371) * math.cos(lat1),
                             math.cos(distance_km / 6371) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return (lat2, lon2)

while True:
    input_str = str(input("Enter the string in the format xxxxxx (or type 'quit' to exit): "))
    if input_str.lower() == 'quit':
        break
    new_coordinates = calculate_new_coordinates(input_str)
    print(f"New coordinates for {input_str}: {new_coordinates}")