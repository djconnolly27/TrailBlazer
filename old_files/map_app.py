"""
Put your Flask app code here.
"""

from flask import Flask
from flask import render_template
from flask import request
import googlemaps
from datetime import datetime
from urllib.request import urlopen
import urllib
import json
import os
import plot_a_route
app = Flask(__name__)

DIRECTIONS_API_KEY = os.environ["DIRECTIONS_KEY"]
GEOCODING_API_KEY = os.environ['GEOCODING_KEY']

GMAP_BASE_URL = "https://www.google.com/maps/embed/v1/place?key="



def initial_URL(formatted_location):
    return GMAP_BASE_URL + DIRECTIONS_API_KEY + "&q=" + formatted_location

def format_location(location):
    return location.replace(" ","+")


@app.route('/')
def home():
    return render_template('home.html')

def findWeather(place):
    from weather import Weather, Unit
    weather = Weather(unit=Unit.FAHRENHEIT)
    # Lookup via location name.
    location = weather.lookup_by_location(place)
    return location

def getCondition(location):
    condition = location.condition
    return condition

def getForcast(location):
# Get weather forecasts for the upcoming days.
    forecasts = location.forecast
    forecast = forecasts[1]
    return forecast


def valid_login(firstname, lastname, email, username, password):
    if firstname == '':
        return False
    if lastname == '':
        return False
    if email == '':
        return False
    if username == '':
        return False
    if password == '':
        return False
    return True


def log_the_user_in(firstname, lastname, location):
    weatherLocation = findWeather(location)
    condition = getCondition(weatherLocation)
    forcast = getForcast(weatherLocation)
    mapURL = initial_URL(format_location(location))
    gmap.draw("templates/my_map.html")
    return render_template('profile.html', firstname=firstname,
    lastname=lastname, location=location, date = condition.date,
    temp=condition.temp, text = condition.text, high = forcast.high, low=forcast.low,
    mapURL = mapURL)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['firstname'],
                        request.form['lastname'],
                        request.form['email'],
                        request.form['username'],
                        request.form['password']):
            with open('storeformdata.txt', 'w') as f:
                f.write(request.form['firstname'])
                f.write(request.form['lastname'])
                f.write(request.form['email'])
                f.write(request.form['username'])
                f.write(request.form['password'])
            return log_the_user_in(request.form['firstname'], request.form['lastname'],request.form['location'])
        else:
            error = 'Missing required information'
    return render_template('error.html', error=error)

@app.route('/makemap', methods=['POST', 'GET'])
def make_map():
    plot_a_route.run(request.form['start'], request.form['distance'])
    return render_template('my_map.html')


if __name__ == '__main__':
    app.run()
