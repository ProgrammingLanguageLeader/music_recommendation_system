# Music recommendation system

This web application enables you to find music recommendations based on your preferences. It uses [Last.fm API](https://www.last.fm/api).

## How to install 
Python 3 interpreter is required. It's recommended to use virtual environment for better isolation.

Install requirements:
```bash
pip install -r requirements.txt # alternatively try pip3
```

Setup environment variables (example on Linux):
```bash
export LASTFM_API_KEY=<your API key>
export LASTFM_API_SECRET=<your API secret>
```

To start the application use this command:
```bash
python manage.py runserver
``` 
