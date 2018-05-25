import re
from django.shortcuts import render

from lastfm_api import LastfmNetwork


def index(request):
    return render(request, 'index.html')


def results(request):
    artist_names = []
    tag_names = []
    track_names = []
    for key, value in request.GET.items():
        if re.match(r'artist_name_\d+', key):
            artist_names.append(value)
        if re.match(r'tag_name_\d+', key):
            tag_names.append(value)
        if re.match(r'track_name_\d+', key):
            track_names.append(value)

    network = LastfmNetwork()
    try:
        recommended_artists = network.get_similar_artists(artist_names[0])
    except KeyError:
        recommended_artists = ['']
    recommended_tracks = ['']
    return render(
        request,
        'results.html',
        context={
            'recommended_artists': recommended_artists,
            'recommended_tracks': recommended_tracks,
        }
    )
