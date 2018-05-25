import os


class Config:
    API_KEY = os.environ.get('LASTFM_API_KEY')
    API_SECRET = os.environ.get('LASTFM_API_SECRET')
