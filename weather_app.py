import plot_a_route as par



def get_weather(place):
    from weather import Weather, Unit
    weather = Weather(unit=Unit.CELSIUS)

    # Lookup via location name.

    location = weather.lookup_by_location(place)
    condition = location.condition
    percip = (condition.text)
    date = (condition.date)
    temp = (condition.temp)

    # Get weather forecasts for the upcoming days.

    forecasts = location.forecast
    forecast = forecasts[1]

    date = (forecast.date)
    high = (forecast.high)
    low = (forecast.low)

if __name__ == "__main__":
    place = input("Enter a place to start: ")
    place = str(place)
    weather = get_weather(place)
