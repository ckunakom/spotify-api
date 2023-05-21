from api.request_token import *

### GET a User's Top Artists and Tracks ###
### -------------------------- ###

def get_top_tracks():
    # base URL of all Spotify API endpoints
    base_url = 'https://api.spotify.com/v1/'

    # user's top track endpoint
    top_track = 'me/top/tracks'
    # Time range value quick guide:
        ## short_term: 4 weeks, medium: 6 months 
        ## long_term: over several year
    time_range = 'time_range=long_term'
    limit = 'limit=25'
    # offset = 'offset=5'

    # Perfrom GET request for data
    global track_json
    track_json = requests.get(base_url + top_track + '?' + time_range + '&' + limit 
    #                           + '&' + offset
                            , headers=headers).json()


get_top_tracks()
# # Save outout as json file to go parse later...
# with open('./data/raw_top_tracks.json', 'w') as outfile:
#     json.dump(track_json, outfile, indent=2)

# ### ------------------------------------------------- ###
# ### -------------------Data Clean Up----------------- ###
# ### ------------------------------------------------- ###

# # Map only the datafields I want
# def track_func2(track):
#     artists_name = [ artist['name']  for artist in track['artists'] ]
#     album_name = track['album']['name']
#     release_date = track['album']['release_date']
#     title = track['name']
#     popularity = track['popularity']
#     duration_ms = track['duration_ms']
#     song_url = track['external_urls']['spotify']

#     return {
#         'title': title,
#         'artists_name': str(artists_name)[2:-2],
#         'album_name':album_name,
#         'release_date':release_date,
#         'duration_min': round(duration_ms/60000, 2),
#         'popularity': popularity,
#         'song_url': song_url
#     }

# # Use map to give a list iterator
# track_list_iterator2 = map(track_func2, track_json['items'])
# # Turn iterator into a list
# track_list2 = list(track_list_iterator2)

# # Export data json
# with open('data/clean_top_tracks.json', 'w') as outfile:
#     json.dump(track_list2, outfile, indent=2)
