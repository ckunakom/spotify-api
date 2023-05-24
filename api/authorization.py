# Dependencies
from config import *
from urllib.parse import urlencode
from collections import OrderedDict
from getpass import getpass

### -------------------------- ###
### --- AUTHORIZATION FLOW --- ### 

### Request User Authorization ###
### -------------------------- ###

# the scope applicable for Read access to a user's top artists and tracks.
# https://developer.spotify.com/documentation/web-api/concepts/scopes
# https://developer.spotify.com/documentation/general/guides/authorization-guide/#list-of-scopes
scope = 'user-top-read'

# Function to log in and request token
def log_in():
    # Enter spotify credentials
    # user_email = getpass(f'Enter username or email: ')
    # user_password = getpass(f'Enter password: ')

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

    print(f'Go log in at {auth_url}')
    print(f'Once logged in, copy the code string from the URL and paste it in the code_from_url on request_token.py')

# Logging in to grab code string
log_in()
