# Dependencies
from dotenv import load_dotenv
import os

# Load all variables
load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')
code_from_url = os.getenv('code_from_url')