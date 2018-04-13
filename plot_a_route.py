'''
Software Design Final Project: Trail Blazer

Intersections.py takes a bounding area, finds all of the paths in that area, and designates the parts of those paths as nodes and edges.
'''

from urllib.request import urlopen
import urllib
import json
import os
import polyline
import gmplot
import math
import random
import geopy
from geopy.distance import VincentyDistance


GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GMAPS_BASE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"
SNAP_TO_ROADS_URL = "https://roads.googleapis.com/v1/snapToRoads"

DIRECTIONS_API_KEY = os.environ["DIRECTIONS_KEY"]
GEOCODING_API_KEY = os.environ['GEOCODING_KEY']

def get_json(url):
    """Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data

def get_nearest_address(lat1, lng1):
    """Given a latitude and longitude, find the nearest address. Accomplishes this by requesting directions from a point to itself, which returns the nearest valid address.
    """
    lat1_str = str(lat1)
    lng1_str = str(lng1)
    origin = lat1_str + ',' + lng1_str
    d = {'origin': origin, 'destination': origin, 'key': DIRECTIONS_API_KEY}
    encoded = urllib.parse.urlencode(d)
    url = GMAPS_BASE_DIRECTIONS_URL + '?' + encoded
    response_data = get_json(url)
    lat = response_data["routes"][0]["legs"][0]["end_location"]['lat']
    lng = response_data["routes"][0]["legs"][0]["end_location"]['lng']
    return lat, lng

#print(get_nearest_address(42.280130, -71.271371))

def get_directions(lat1, lng1, lat2, lng2):
    """Find directions between points.
    """
    lat1_str = str(lat1)
    lng1_str = str(lng1)
    lat2_str = str(lat2)
    lng2_str = str(lng2)
    origin = lat1_str + ',' + lng1_str
    destination = lat2_str + ',' + lng2_str
    d = {'origin': origin, 'destination': destination, 'mode': 'walking', 'key': DIRECTIONS_API_KEY}
    encoded = urllib.parse.urlencode(d)
    url = GMAPS_BASE_DIRECTIONS_URL + '?' + encoded
    response_data = get_json(url)
    return response_data

def get_total_distance(response_data):
    ''' Finds the total distance of a route. '''
    total_distance = response_data["routes"][0]["legs"][0]["distance"]["text"]
    return total_distance

def get_decoded_polyline(response_data):
    ''' Decodes an encoded polyline and returns a list of lat, lng points along a route'''
    encoded_polyline = response_data["routes"][0]["overview_polyline"]["points"]
    decoded = polyline.decode(encoded_polyline)
    return decoded

def miles_to_km(miles):
    ''' Converts a distance from miles to kilometers '''
    one_mile_in_km = 1.609344
    return miles * one_mile_in_km

def get_lat_long(place_name):
    """Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.
    """
    d = {'address': place_name, 'key': GEOCODING_API_KEY}
    encoded = urllib.parse.urlencode(d)
    url = GMAPS_BASE_URL + '?' + encoded
    response_data = get_json(url)
    #print(response_data)
    #print(response_data['results'][0]['geometry']['location'])
    coords = response_data["results"][0]['geometry']['location']
    #print(coords)
    lat = coords['lat']
    lng = coords['lng']
    return lat, lng

#print(get_directions(42.280130, -71.271371, 42.280267, -71.234833))

def find_new_lat_lng_geopy(lat, lng, b, dist): #b in degrees (0 is north, 90 is east), dist=distance in kilometers
    ''' Uses geopy to find a point an 'as-the-crow-flies' distance from a given origin point '''
    origin = geopy.Point(lat, lng)
    destination = VincentyDistance(kilometers=dist).destination(origin, b)
    return (destination.latitude, destination.longitude)

def get_a_random_desination(lat, lng, dist, num_points):
    ''' Chooses a random destination by finding num_points potential destinations and randomly selecting one. '''
    bearing = 0
    bearing_increase = 360/num_points
    points_on_circumference = []
    for i in range(num_points):
        points_on_circumference.append(find_new_lat_lng_geopy(lat, lng, bearing, dist))
        bearing += bearing_increase
    return random.choice(points_on_circumference)
#print(find_new_lat_lng_geopy(42.293051, -71.264902, 180, 10))


def find_center(single_run):
    ''' Finds the center of the route by averaging the latitude and longitude coordinates of the route '''
    total_lats = 0
    total_lngs = 0
    counter = 0
    for coord in single_run:
        total_lats += coord[0]
        total_lngs += coord[1]
        counter += 1
    center = (total_lats/counter, total_lngs/counter)
    return(center)

def get_a_route(place_name, distance):
    ''' Get a random route that that starts at a given point and ends at a point a given 'as-the-crow-flies' distance from that starting point. '''
    init_coords = (init_lat, init_lng) = get_lat_long(place_name)
    destination = get_a_random_desination(init_lat, init_lng, distance, 8)
    dest_address = get_nearest_address(destination[0], destination[1])
    directions = get_directions(init_lat, init_lng, dest_address[0], dest_address[1])
    route = get_decoded_polyline(directions)
    distance = get_total_distance(directions)
    #print(route)
    #center = find_center(route)
    #print(center)
    return route, distance

def run(place, distance):
    ''' Allows plot_a_route.py to be run as a module in another file '''
    place = str(place)
    distance = float(distance)
    the_route = get_a_route(place, distance)
    center = find_center(the_route)
    gmap = gmplot.GoogleMapPlotter(center[0], center[1], 10)

    path_lats, path_lngs = zip(*the_route)
    gmap.plot(path_lats, path_lngs, 'cornflowerblue', edge_width=10)

    # Draw
    gmap.draw("templates/my_map.html")


if __name__ == "__main__":
    place = input("Enter a place to start: ")
    place = str(place)
    distance = input("Enter a distance: ")
    distance = float(distance)
    route_info = get_a_route(place, distance)
    the_route = route_info[0]
    center = find_center(the_route)
    #print(route_info[1])
    gmap = gmplot.GoogleMapPlotter(center[0], center[1], 10)

    path_lats, path_lngs = zip(*the_route)
    gmap.plot(path_lats, path_lngs, 'cornflowerblue', edge_width=10)

    # Draw
    gmap.draw("templates/my_map.html")
