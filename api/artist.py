# Dependencies
import json
import pandas as pd
import requests
from top_tracks import *

# Define empty array for ids
artist_ids = []

# Loop through track_json from top_tracks endpoint
artist_data = track_json['items']

for artist in artist_data:
    item = artist['album']['artists']
    for i in item:
        id = i['id']
        # No duplicate artist shall make it to the array
        if id in artist_ids:
            continue
        else:
            artist_ids.append(id)

### GET Artists from prior request ###
### -------------------------- ###
artist_url = 'https://api.spotify.com/v1/artists/'
# artist endpoint -- artists/{id}

# Time to loop through
artist_json = []

for id in artist_ids:
    # Perfrom GET request for data
    artist_resp = requests.get(artist_url + id
                            , headers=headers).json()
    artist_json.append(artist_resp)

# Save outout as json file to go parse later...
with open('../data/raw_artists.json', 'w') as outfile:
    json.dump(artist_json, outfile, indent=2)
