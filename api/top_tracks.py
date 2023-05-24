from request_token import *
import json

### GET a User's Top Artists and Tracks ###
### -------------------------- ###

def get_top_tracks():
    # base URL of all Spotify API endpoints
    base_url = 'https://api.spotify.com/v1/'

    # user's top track endpoint
    top_track = 'me/top/tracks'
    # Time range value quick guide:
        ## short_term: 4 weeks, medium_term: 6 months 
        ## long_term: over several year
    time_range = 'time_range=medium_term'
    limit = 'limit=50'
    # offset = 'offset=5'

    # Perfrom GET request for data
    global track_json
    track_json = requests.get(base_url + top_track + '?' + time_range + '&' + limit 
    #                           + '&' + offset
                            , headers=headers).json()


get_top_tracks()

# Save outout as json file to go parse later...
with open('../data/raw_top_tracks.json', 'w') as outfile:
    json.dump(track_json, outfile, indent=2)
