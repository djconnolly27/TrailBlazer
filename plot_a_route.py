from urllib.request import urlopen
import urllib
import json
import os
import polyline


GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GMAPS_BASE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"
SNAP_TO_ROADS_URL = "https://roads.googleapis.com/v1/snapToRoads"

DIRECTIONS_API_KEY = os.environ["DIRECTIONS_KEY"]

def get_json(url):
    """Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data


#request directions from a point to itself, which returns the nearest valid address.
def get_nearest_address(lat1, lng1):
    """Given a latitude and longitude, find the nearest address.
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
    encoded_polyline = response_data["routes"][0]["overview_polyline"]["points"]
    decoded = polyline.decode(encoded_polyline)
    return decoded


def get_lat_long(place_name):
    """Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    d = {'address': place_name}
    encoded = urllib.parse.urlencode(d)
    url = GMAPS_BASE_URL + '?' + encoded
    response_data = get_json(url)
    lat =response_data["results"][0]['geometry']['location']['lat']
    lng =response_data["results"][0]['geometry']['location']['lng']
    return lat, lng

#print(get_directions(42.280130, -71.271371, 42.280267, -71.234833))

import gmplot
import math
import random

#I implemented the following function using formulas on wikipedia for the VincentyDistance between two points, the latitude portion does not currently work. I then found geopy and used that instead.
def find_new_lat_lng(lat, lng, direction, s): #using VincentyDistance
    phi1 = math.radians(lat)
    L1 = math.radians(lng)
    alpha1 = math.radians(direction)
    a = 6378137.0 #meters
    f = 1/298.257223563
    b = 6356752.314245 #meters
    phi1 = phi1 #latitude of point1
    #phi2 = #latitude of point 2
    U1 = math.atan((1-f)*math.tan(phi1)) #reduced latitude
    #U2 = math.atan((1-f)*math.tan(phi2)) #reduced latitude
    #L = #L2 - L1 (diff in longitude of two points)
    #lambda1 = #longitude of point 1 on auxiliary sphere
    #lambda2 = #longitude of point 2 on auxiliary sphere
    alpha1 = alpha1#forward azimuth at point 1
    #alpha2 = #forward azimuth at point 2
    s = s#ellipsoidal distance between the two points
    sigma1 = math.atan(math.tan(U1)/math.cos(alpha1))
    sin_alpha = math.cos(U1)*math.sin(alpha1)
    cos_squared_alpha = 1 - sin_alpha**2
    u_squared = cos_squared_alpha*((a**2 - b**2)/(b**2))
    A = 1 + (u_squared/16384)*(4096 + u_squared*(-768 + u_squared*(320 - 175*u_squared)))
    B = (u_squared/1024)*(256 + u_squared*(-128 + u_squared*(74 - 47*u_squared)))
    sigma = s/(b*A) #arc length between points
    epsilon = 0.00001
    end_sigma = 0
    state = True
    two_sigma_m = 0
    while(state):
        sigma_start = sigma
        if (end_sigma - sigma_start) < epsilon:
            state = False
        else:
            two_sigma_m = 2*sigma1 + sigma
            delta_sigma = B*math.sin(sigma)*(math.cos(two_sigma_m) + (1/4)*B*(math.cos(sigma)*(-1 + 2*(math.cos(two_sigma_m)**2)) - (B/6)*math.cos(two_sigma_m)*(-3 + 4*(math.sin(sigma)**2))*(-3 + 4*(math.cos(two_sigma_m)**2))))
            sigma = sigma + delta_sigma
            end_sigma = sigma
    phi2 = math.atan((math.sin(U1)*math.cos(sigma) + math.cos(U1)*math.sin(sigma)*math.cos(alpha1))/(1-f)*math.sqrt(sin_alpha**2 + ((math.sin(U1)*math.sin(sigma) - math.cos(U1)*math.cos(sigma)*math.cos(alpha1))**2)))
    the_lambda = math.atan((math.sin(sigma)*math.sin(alpha1))/(math.cos(U1)*math.cos(sigma) - math.sin(U1)*math.sin(sigma)*math.cos(alpha1)))
    C = (f/16)*cos_squared_alpha*(4 + f*(4 - 3*cos_squared_alpha))
    L = the_lambda - (1 - C)*f*sin_alpha*(sigma + C*sin_alpha*(math.cos(two_sigma_m) + C*math.cos(sigma)*(-1 + 2*(math.cos(two_sigma_m)**2))))
    L2 = L + L1
    new_lat = math.degrees(phi2)
    new_lng = math.degrees(L2)
    return new_lat, new_lng

import geopy
from geopy.distance import VincentyDistance

def find_new_lat_lng_geopy(lat, lng, b, dist): #b in degrees (0 is north, 90 is east), dist=distance in kilometers
    origin = geopy.Point(lat, lng)
    destination = VincentyDistance(kilometers=dist).destination(origin, b)
    return (destination.latitude, destination.longitude)

def get_a_random_desination(lat, lng, dist, num_points):
    bearing = 0
    bearing_increase = 360/num_points
    points_on_circumference = []
    for i in range(num_points - 1):
        points_on_circumference.append(find_new_lat_lng_geopy(lat, lng, bearing, dist))
        bearing += bearing_increase
    return random.choice(points_on_circumference)
#print(find_new_lat_lng_geopy(42.293051, -71.264902, 180, 10))


def find_center(single_run):
    total_lats = 0
    total_lngs = 0
    counter = 0
    #print(single_run)
    for coord in single_run:
        total_lats += coord[0]
        total_lngs += coord[1]
        counter += 1
    center = (total_lats/counter, total_lngs/counter)
    return(center)

def get_a_route(place_name, distance):
    init_coords = (init_lat, init_lng) = get_lat_long(place_name)
    destination = get_a_random_desination(init_lat, init_lng, distance, 8)
    dest_address = get_nearest_address(destination[0], destination[1])
    route = get_directions(init_lat, init_lng, dest_address[0], dest_address[1])
    #print(route)
    #center = find_center(route)
    #print(center)
    return route

# print(get_lat_long('Olin College'))
# init_coords = (init_lat, init_lng) = get_lat_long('Olin College')
# print(init_lat)
# print(init_lng)
# # init_lat = (get_lat_long('1000 Olin Way, Needham')[0])
# # print(init_lat)
# # init_lng = (get_lat_long('1000 Olin Way, Needham')[1])
# # print(init_lng)
# destination = get_a_random_desination(init_lat, init_lng, 10, 8)
# dest_address = get_nearest_address(destination[0], destination[1])
# print(dest_address)
# get_directions((init_lat), (init_lng), (dest_address[0]), (dest_address[1]))
# Place map
the_route = get_a_route('Olin College', 10)
center = find_center(the_route)
gmap = gmplot.GoogleMapPlotter(center[0], center[1], 10)

path_lats, path_lngs = zip(*the_route)
gmap.plot(path_lats, path_lngs, 'cornflowerblue', edge_width=10)

# Draw
gmap.draw("templates/my_map.html")
