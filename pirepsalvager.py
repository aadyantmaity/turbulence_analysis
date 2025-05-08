import math

def calculate_coordinates(degrees, nautical_miles):
    lax_lat = 33.94312
    lax_lon = -118.40880

    degrees_rad = math.radians(degrees)
    distance_km = nautical_miles * 1.852
    earth_radius_km = 6371.0

    new_lat = math.asin(math.sin(math.radians(lax_lat)) * math.cos(distance_km / earth_radius_km) +
                        math.cos(math.radians(lax_lat)) * math.sin(distance_km / earth_radius_km) * math.cos(degrees_rad))

    new_lon = math.radians(lax_lon) + math.atan2(math.sin(degrees_rad) * math.sin(distance_km / earth_radius_km) * math.cos(math.radians(lax_lat)),
                                                 math.cos(distance_km / earth_radius_km) - math.sin(math.radians(lax_lat)) * math.sin(new_lat))

    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    return round(new_lat, 5), round(new_lon, 5)

def calculate_multiple_coordinates(coordinates_list):
    results = []
    for degrees, nautical_miles in coordinates_list:
        results.append(calculate_coordinates(degrees, nautical_miles))
    return results

coordinates_list = [(71, 7), (70, 3), (70, 3), (140, 10), 
                    (70, 5), (71, 3), (71, 5), (71, 7), 
                    (71, 2), (70, 5), (180, 25), (80, 10), 
                    (50, 10), (90, 25), (70, 20), (90, 15), 
                    (90, 50)]
new_coordinates_list = calculate_multiple_coordinates(coordinates_list)
print(f"New coordinates list: {new_coordinates_list}")