# Trail Blazer
Final Project Route Finding App
By Daniel Connolly, Raquel Dunoff, and Lydia Hodges

### Description
Trail Blazer will help generate and visualize new routes for runners, walkers, and bikers. We are creating this for our Software Design final project.

### Modules
To run our program, please install the following modules:

GMPlot - run the following in the command line: pip install gmplot

Flask - run the following in the command line: conda install Flask

Geopy - run the following in the command line: pip install geopy

Geographiclib - run the following in the command line: pip install geographiclib

Polyline - run the following in the command line: pip install polyline

Overpy - run the following in the command line: pip install overpy

Weather API - run the following in the command line: pip install weather-api

You will also need to get a Google Maps Directions API key as well as a Google Maps Geocoding API key and run the following in the command line:
export GEOCODING_KEY = your_geocoding_key
export DIRECTIONS_KEY = your_directions_key

You can obtain a geocoding key from https://developers.google.com/maps/documentation/geocoding/intro

You can obtain a directions key from https://developers.google.com/maps/documentation/directions/



### Running the Program
Our code is broken up into several different files at the moment, including intersections.py, plot_a_route.py, weather_app.py, and map_app.py. Map_app.py will run plot_a_route.py as a module, but the other files run independently of one another at the moment.

To access the web app you can run weather_app.py and click the link to the web app that it returns. The other files are linked throughout the web app by submitting forms. 

