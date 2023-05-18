# Dependencies
import requests
import json
import pandas as pd
from pprint import pprint
from config import *
# from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from collections import OrderedDict
from getpass import getpass

### -------------------------- ###
### --- AUTHORIZATION FLOW --- ### 

### Request User Authorization ###
### -------------------------- ###
# Build URL to request user authorization
redirect_uri = 'https://google.com/callback'

# the scope applicable for Read access to a user's top artists and tracks.
# https://developer.spotify.com/documentation/web-api/concepts/scopes
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

### LET CHROME DRIVER DO THE WORK ###
# Creating a path for chromedriver on windows
## Update the path for chromedriver accordingly
## Splinter
# executable_path = {'executable_path': r'c:\bin\chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

# launch the url with chrome driver
# browser.visit(auth_url)

## Selenium
driver = webdriver.Chrome(executable_path=r'c:\bin\chromedriver.exe')
# launch the url with chrome driver
driver.get(auth_url)

# Enter spotify credentials
# user_email = getpass(f'Enter username or email: ')
# user_password = getpass(f'Enter password: ')

# Fill login info (need to get html id for username and password for below)
## Splinter
# browser.find_by_id('login-username').fill(user_email)
# browser.find_by_id('login-password').fill(user_password)

## Selenium
driver.find_element(By.ID,'login-username').send_keys(user_email)
driver.find_element(By.ID,'login-password').send_keys(user_password)

# Click the 'Log in' button
# button = browser.find_by_id('login-button') ## Splinter
button = driver.find_element(By.ID,'login-button') ## Selenium
button.click()
# Give it time to pop up another page
time.sleep(5)

# Click 'Agree' button
# button = browser.find_by_xpath("//button[@data-testid='auth-accept']") ## Splinter
button = driver.find_element(By.XPATH, "//button[@data-testid='auth-accept']") ## Selenium
button.click()
# Give it time to change page again
time.sleep(5)

# Get the current url
# logged_in_url = browser.url ## Splinter
logged_in_url = driver.current_url ## Selenium

# url for spotify api
parsed_url = urlparse(logged_in_url)
code_from_url = parse_qs(parsed_url.query)['code'][0]

# Shut the browser down
# browser.quit()  ## Splinter
driver.close() ## Selenium

### CHROME DRIVER SHUT DOWN ###

############################################## pause here, clean up later

### Request Access Token ###
### -------------------------- ###

# Make POST request to Spotify on /api/token endpoint

# Define required parameter
request_url = 'https://accounts.spotify.com/api/token'
request_body_parameter = {
    'grant_type': 'authorization_code',
    'code': code_from_url,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret,
}

# POST request with body + parameter
auth_response = requests.post(request_url, request_body_parameter)

# convert the response to JSON
auth_response_data = auth_response.json()

# Save the access token
access_token = auth_response_data['access_token']
# Save the refresh token
refresh_token = auth_response_data['refresh_token']

### GET a User's Top Artists and Tracks ###
### -------------------------- ###

# Define headers with access_token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# base URL of all Spotify API endpoints
base_url = 'https://api.spotify.com/v1/'

# user's top track endpoint
top_track = 'me/top/tracks'
time_range = 'time_range=long_term'
limit = 'limit=50'
# offset = 'offset=5'

# Perfrom GET request for data
track_json = requests.get(base_url + top_track + '?' + time_range + '&' + limit 
#                           + '&' + offset
                          , headers=headers).json()

# Save outout as json file to go parse later...
with open('data/raw_top_tracks.json', 'w') as outfile:
    json.dump(track_json, outfile, indent=2)

### ----- When token expires: REFRESH TOKEN---------- ### 
### ------------------------------------------------- ###
# Base 64 encoded string that contains the client ID and client secret key.
import base64

def encode_base64(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii') 
    return base64_message
#     return str(base64_bytes, "utf-8")
    
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
    
    request_access_token = requests.post(request_url, body, headers=header)
    request_access_token_data = request_access_token.json()

    # Update access_token
    return request_access_token_data['access_token']

# Update access token from Step 3
access_token = refresh_access_token()

# Update headers
headers = {'Authorization': f'Bearer {access_token}'}

### Data Clean Up --> maybe move this to another file :/

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


# Exporat data to JSON
with open('data/clean_top_tracks.json', 'w') as outfile:
    json.dump(track_list, outfile, indent=2)

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
