'''
Software Design Final Project: Trail Blazer

get_elevtions.py finds a list of elevations from the longitude and lattitude coordinates using the Google Maps API and plots it using matplotlib.
'''
import googlemaps
from datetime import datetime
from googlemaps import convert
import matplotlib.pyplot as plt
import numpy as np

import os

GEOCODING_API_KEY = "AIzaSyA4WtBU35L_hml2GTdqtLbHk-IXd76dRuw"
ELEVATION_API_KEY = "AIzaSyCuHDqWKO7-zWFrU5qhWsaLydNk1mhvaPY"

gmaps = googlemaps.Client(key=GEOCODING_API_KEY) #Creates google map

def get_elevation_list(lats=(42.293114, 42.292670, 42.291980, 42.291908, 42.292519,42.292354, 42.293600, 42.295283, 42.296575),longs=(-71.264425, -71.263695, -71.263760, -71.262730, -71.261625,-71.261099,-71.260166,-71.259657, -71.260000)):
    """Defines the longitude and lattitude coordinates in lists.
    Fills elevations with a list of corresponding elevations.
    """
    lats = lats
    longs = longs
    elevations = []

    #Populate elevations
    for i in range(len(lats)):
        lat_long = (lats[i],longs[i]) #Format lattitute and longitude
        elevationData = gmaps.elevation(lat_long) #Get the JSON files from the Google Maps API
        elevation = elevationData[0]['elevation'] #Extract the elevation
        elevations.append(elevation) #add the elevation to the list
    return elevations

def plot_elevation(elevations):
    plt.plot(elevations,color = 'g')
    plt.fill_between(np.linspace(0,8,num=9),elevations,0,alpha=0.5, color='g')
    plt.show()

if __name__ == '__main__':
    plot_elevation(get_elevation_list())
