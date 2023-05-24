from config import *
import requests

# Paste the code string copied from the URL after logging in
code_from_url = ''

def request_token():
    ### Request Access Token ###
    ### -------------------------- ###

    # Make POST request to Spotify on /api/token endpoint
    # Define required parameter
    request_url = "https://accounts.spotify.com/api/token"
    request_body_parameter = {
        "grant_type": "authorization_code",
        "code": code_from_url,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # POST request with body + parameter
    auth_response = requests.post(request_url, request_body_parameter)

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # Save the access token
    global access_token
    access_token = auth_response_data["access_token"]
    # Save the refresh token
    refresh_token = auth_response_data["refresh_token"]

    global headers
    headers = {"Authorization": f"Bearer {access_token}"}

request_token()
print('Headers has been defined.')