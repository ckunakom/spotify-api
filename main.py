# Dependencies
import requests
import json
import pandas as pd
from pprint import pprint
from api.config import *
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
# https://developer.spotify.com/documentation/general/guides/authorization-guide/#list-of-scopes
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

# Enter spotify credentials
user_email = getpass(f'Enter username or email: ')
user_password = getpass(f'Enter password: ')

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

# Fill login info with user's input
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

### ---CHROME DRIVER SHUT DOWN ---###

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
''' short_term: 4 weeks 
    medium_term: 6 months 
    long_term: over several year '''
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
'''artist endpoint: artists/{id}'''

# Time to loop through
artist_json = []

for id in artist_ids:
    # Perfrom GET request for data
    artist_resp = requests.get(artist_url + id
                            , headers=headers).json()
    artist_json.append(artist_resp)

# Save output as json file to go parse later...
with open('data/raw_artists.json', 'w') as outfile:
    json.dump(artist_json, outfile, indent=2)

print('Data Extractioon is complete. Run data_cleaning.py next.')