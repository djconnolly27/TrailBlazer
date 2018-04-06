import requests
import os
import polyline
import random
from gmplot import gmplot

#In the terminal, run "export TOKEN=(insert_your_api_key)"
token = os.environ["TOKEN"]
headers = {'Authorization': "Bearer {0}".format(token)}
segments = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(1), headers = headers)
seg_json = segments.json()

paths = []
for segment in seg_json:
    encoded_coords = segment['map']['summary_polyline']
    if encoded_coords != None:
        paths.append(polyline.decode(encoded_coords))


def find_center(single_run):
    total_lats = 0
    total_lngs = 0
    counter = 0
    for coord in single_run:
        total_lats += coord[0]
        total_lngs += coord[1]
        counter += 1
    center = (total_lats/counter, total_lngs/counter)
    return(center)


# Place map
gmap = gmplot.GoogleMapPlotter(find_center(paths[0])[0], find_center(paths[0])[1], 13)

area_lats, area_lngs = zip(*paths[0])

gmap.plot(area_lats, area_lngs, 'cornflowerblue', edge_width=10)



# Draw
gmap.draw("my_map.html")
