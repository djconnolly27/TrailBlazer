'''
Software Design Final Project: Trail Blazer

get_start_point.py finds a starting location from a user specified point on a google map embedded on profile.html to return a lattitude and longitude starting coordinate.
'''
import googlemaps
from datetime import datetime
from googlemaps import convert

import os

GMAP_BASE_URL = "https://www.google.com/maps/embed/v1/place?key="

DIRECTIONS_API_KEY = os.environ["DIRECTIONS_KEY"]
GEOCODING_API_KEY = os.environ['GEOCODING_KEY']
ELEVATION_API_KEY = os.environ['ELEVATION_KEY']

gmaps = googlemaps.Client(key=GEOCODING_API_KEY)

geocode_result = gmaps.geocode('Olin College of Engineering')


LOCATION = "Olin College"


def initial_URL(formatted_location):
    return GMAP_BASE_URL + DIRECTIONS_API_KEY + "&q=" + formatted_location


def format_location(location):
    return location.replace(" ","+")


if __name__ == '__main__':
    lats = (42.293114, 42.292670, 42.291980, 42.291908, 42.292519,42.292354, 42.293600, 42.295283, 42.296575)
    longs = (-71.264425, -71.263695, -71.263760, -71.262730, -71.261625,-71.261099,-71.260166,-71.259657, -71.260000)
    lat_long = []

    for i in range(len(lats)):
        lat_long = (lats[i],longs[i])
    print(lat_long)

    lat_long_list= []

    for i in range(len(lats)):
        coord_tuple =  [lats[i] , longs[i]]
        lat_long_list += coord_tuple

    print(lat_long_list)
    gmaps.elevation(lat_long)
    #gmaps.elevation_along_path(lat_long_list,10)
