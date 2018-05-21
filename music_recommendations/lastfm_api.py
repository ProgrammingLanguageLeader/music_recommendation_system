import pylast
import os

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')

network = pylast.LastFMNetwork(
    api_secret=API_SECRET,
    api_key=API_KEY
)
