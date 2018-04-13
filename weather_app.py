import plot_a_route as par


class climate:

    def __init__(self, percip=0,date=0,temp=0,high=0,low=0):
        from weather import Weather, Unit
        weather = Weather(unit=Unit.CELSIUS)

    # Lookup via location name.

        location = weather.lookup_by_location(place)
        condition = location.condition
        self.percip = (condition.text)
        self.date = (condition.date)
        self.temp = (condition.temp)

    # Get weather forecasts for the upcoming days.

        forecasts = location.forecast
        forecast = forecasts[1]


        self.high = (forecast.high)
        self.low = (forecast.low)

if __name__ == "__main__":
    #place = input("Enter a place to start: ")
    #place = str(place)
    place = "Olin College"
    weather = climate(place)
    print(weather.date)
