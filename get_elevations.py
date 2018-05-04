'''
Software Design Final Project: Trail Blazer

Get_elevations finds the elevations of lat-lng point along a route using the Google Maps API and plots the elevations accordingly.
'''
from googlemaps import Client as client
import matplotlib.pyplot as plt
import numpy as np

GEOCODING_API_KEY = "AIzaSyA4WtBU35L_hml2GTdqtLbHk-IXd76dRuw"
ELEVATION_API_KEY = "AIzaSyCuHDqWKO7-zWFrU5qhWsaLydNk1mhvaPY"

def get_elevation_list(lats, longs):
    """Defines the longitude and lattitude coordinates in lists. Fills elevations with a list of corresponding elevations.
    """
    elevations = []

    map_client = client(key=GEOCODING_API_KEY)

    #Populate elevations
    for i in range(len(lats)):
        lat_long = (lats[i], longs[i]) #Format lattitute and longitude
        elevation_data = map_client.elevation(lat_long) #Get the JSON files from the Google Maps API
        elevation = elevation_data[0]['elevation'] #Extract the elevation
        elevations.append(elevation) #add the elevation to the list
    return elevations

def plot_elevation(elevations, distance):
    ''' Plots the elevations of points along a route over the course of the route. '''
    x_axis = np.linspace(0, distance, num=len(elevations))
    plt.plot(x_axis, elevations, color='g')
    plt.fill_between(x_axis, elevations, 0, alpha=0.5, color='g')
    plt.show()
