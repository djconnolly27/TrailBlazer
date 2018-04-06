import requests
import os
import polyline
import random
token = os.environ["TOKEN"]
headers = {'Authorization': "Bearer {0}".format(token)}
segments = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(1), headers = headers)
seg_json = segments.json()

print(seg_json)
for segment in seg_json:
    encoded_coords = segment['map']['summary_polyline']
    if encoded_coords != None:
        #print(encoded_coords)
        print(polyline.decode(encoded_coords))
