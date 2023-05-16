# Dependencies
import requests
import json
import pandas as pd
from pprint import pprint
from config import *
from splinter import Browser
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from collections import OrderedDict

 
# https://developer.spotify.com/documentation/general/guides/authorization-guide/#list-of-scopes

# Build URL to request user authorization
redirect_uri = 'https://google.com/callback'

# the scope applicable for Read access to a user's top artists and tracks.
scope = 'user-top-read'

auth_param = {
    'response_type': 'code',
    'client_id': client_id,
    'scope': scope,
    'redirect_uri': redirect_uri,
    'show_dialog': 'true'
}

url_str = 'https://accounts.spotify.com/authorize?'

# piece it together
query_string = urlencode(OrderedDict(auth_param))
auth_url = url_str + query_string 


# Creating a path for chromedriver on windows
executable_path = {'executable_path': 'c:/bin/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# launch the url with chrome driver
browser.visit(auth_url)

# Fill login info (need to get html id for username and password for below)
browser.find_by_id('login-username').fill(user_email)
browser.find_by_id('login-password').fill(user_password)


# Click the 'Log in' button
button = browser.find_by_id('login-button')
button.click()


# Click 'Agree' button
button = browser.find_by_xpath("//button[@data-testid='auth-accept']")
button.click()

# Print the current url
logged_in_url = browser.url

# url for spotify api
parsed_url = urlparse(logged_in_url)
code_from_url = parse_qs(parsed_url.query)['code'][0]

# Shut the browser down
browser.quit()


# CLEANED UP UNTIL HERE --- SAVE POINT!

# ## Authorization flow

# Step 1: Request authorization to access data. No code. 
# - Example Grant access URL:
# https://accounts.spotify.com/authorize?response_type=code&client_id=5d67ef47a63a42f08feb4c824ee174f7&scope=user-top-read&redirect_uri=https%3A%2F%2Fgoogle.com%2Fcallback&show_dialog=true
# 
# Once accept, data can now be requested.
# 
# Note: if changing `scope`, this step and step 2 need to be repeated.
# Scope for the following:
# - User's Top Artists and Tracks: `user-top-read`
# - List of a User's Playlists: `playlist-read-private`

# Step 2: Request to get refresh and access token
# - Make POST request to Spotify on /api/token endpoint
# - Require parameters specfied accordingly.

# In[14]:


# POST - REQUEST BODY PARAMETER, skipping header parameter using alternative way
request_body_parameter = {
    'grant_type': 'authorization_code',
    'code': code_from_url,
    'redirect_uri': 'https://google.com/callback',
    'client_id': client_id,
    'client_secret': client_secret,
}


# In[15]:


# Pass an access token - POST a request with client credentials and save part of response
request_url = 'https://accounts.spotify.com/api/token'

# POST - REQUEST BODY PARAMETER
auth_response = requests.post(request_url, request_body_parameter)

# convert the response to JSON
auth_response_data = auth_response.json()

# Try print it out to get refresh_token - oh oops, don't print it out :P 
# print(auth_response_data)


# In[16]:


# Save the access token
access_token = auth_response_data['access_token']

# Save the refresh token
refresh_token = auth_response_data['refresh_token']


# Step 3: Use access token to access data of interests(?)
# - Note: when access token expires, it can't be used anymore.

# #### Get a User's Top Artists and Tracks

# In[17]:


# Form GET request to API server with access_token in the header
headers = {
    'Authorization': f'Bearer {access_token}'
}

# base URL of all Spotify API endpoints
base_url = 'https://api.spotify.com/v1/'

# user's top track
top_track = 'me/top/tracks'
time_range = 'time_range=medium_term'
limit = 'limit=50'
# offset = 'offset=0'


# ##### If token expires, go to Step 4 (scroll down) and run those code; otherwise, skip

# In[19]:


# Perfrom a request for data
track_json = requests.get(base_url + top_track + '?' + time_range + '&' + limit 
#                           + '&' + offset
                          , headers=headers).json()


# In[20]:


# Save outout as json file to go parse later...
with open('data/raw_top_tracks.json', 'w') as outfile:
    json.dump(track_json, outfile, indent=2)


# Step 4: When access token expires, refresh token to the rescue (from step 2)

# In[ ]:


# Base 64 encoded string that contains the client ID and client secret key.
import base64

def encode_base64(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii') 
    return base64_message
#     return str(base64_bytes, "utf-8")
    
print(encode_base64(f'{client_id}:{client_secret}'))


# In[ ]:


# Get the new refresh access token and update - only when request fails 
def refresh_access_token():   
    # build body parameter
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    
    # base64 string from above encode_base64 function
    auth_base64 = encode_base64(f'{client_id}:{client_secret}')
    
    # build header parameter
    header = {
        'Authorization': f'Basic {auth_base64}'
    }
    
    request_access_token = requests.post(AUTH_URL, body, headers=header)
    request_access_token_data = request_access_token.json()
    print(request_access_token_data)
    # Update access_token (for step 3)
    return request_access_token_data['access_token']


# In[ ]:


# Update access token from Step 3
access_token = refresh_access_token()

# Update headers
headers = {'Authorization': f'Bearer {access_token}'}


# # Data Clean Up

# Note to self: Write a function that uses map to take the data in array (either array of array or array of object, etc) and apply it in each item in an array - Return me an array from an array with only the pieces I want
# 
# Instead of define a bunch of empty lists and create a loop to append each item in to each list, this is much cleaner and more efficient

# In[ ]:


# Map only the datafields I want
def track_func(track):
#artists = [artist['name'] for artist in track['artists']]
# artist['name']
# { 'id': artist['id'], 'name': artist['name'] }
    artists_id = [  artist['id']  for artist in track['artists'] ]
    artists_name = [ artist['name']  for artist in track['artists'] ]
    album_id = track['album']['id']
    album_name = track['album']['name']
    release_date = track['album']['release_date']
    song_id = track['id']
    title = track['name']
    popularity = track['popularity']
    duration_ms = track['duration_ms']
    song_url = track['external_urls']['spotify']

    return {
        'song_id': song_id,
        'title': title,
        'artists_id': str(artists_id)[2:-2],
        'artists_name': str(artists_name)[2:-2],
        'album_id': album_id,
        'album_name':album_name,
        'release_date':release_date,
        'duration_min': round(duration_ms/60000, 2),
        'popularity': popularity,
        'song_url': song_url
        
    }
# Use map to give a list iterator
track_list_iterator = map(track_func, track_json['items'])
# Turn iterator into a list
track_list = list(track_list_iterator)
track_list


# In[ ]:


track_json


# In[ ]:


# Exporat data to JSON
with open('data/clean_top_tracks.json', 'w') as outfile:
    json.dump(track_list, outfile, indent=2)
    
# Wahh!! Beautiful!


# In[ ]:


# Map only the datafields I want v2 - Combining artists of there's more than 1 artist
def track_func2(track):
    artists_name = [ artist['name']  for artist in track['artists'] ]
    album_name = track['album']['name']
    release_date = track['album']['release_date']
    title = track['name']
    popularity = track['popularity']
    duration_ms = track['duration_ms']
    song_url = track['external_urls']['spotify']

    return {
        'title': title,
        'artists_name': str(artists_name)[2:-2],
        'album_name':album_name,
        'release_date':release_date,
        'duration_min': round(duration_ms/60000, 2),
        'popularity': popularity,
        'song_url': song_url
    }

# Use map to give a list iterator
track_list_iterator2 = map(track_func2, track_json['items'])
# Turn iterator into a list
track_list2 = list(track_list_iterator2)

# I need a v2 to serve my immediate purpose
with open('data/clean_top_tracks.json', 'w') as outfile:
    json.dump(track_list2, outfile, indent=2)


# In[ ]:


# Convert the array of data into a dataframe just to look at it
top_tracks_df = pd.DataFrame(track_list)
top_tracks_df

