import re
from django.shortcuts import render

from lastfm_api import LastfmNetwork


def index(request):
    return render(request, 'index.html')


def results(request):
    artists_limit = 20
    tracks_limit = 60

    try:
        recommend_by = request.GET['recommend_by']
    except KeyError:
        recommend_by = ''
    artists_names = []
    tags_names = []
    tracks_names = []
    for key, value in request.GET.items():
        if re.match(r'artist_name_\d+', key) and value:
            artists_names.append(value)
        if re.match(r'tag_name_\d+', key) and value:
            tags_names.append(value)
        if re.match(r'track_name_\d+', key) and value:
            tracks_names.append(value)

    network = LastfmNetwork()
    recommended_artists = []
    recommended_tracks = []
    if recommend_by == 'artists':
        similar_artists = network.fetch_similar_artists(
            artists_names=artists_names,
            limit=10
        )
        recommended_artists = network.sort_artists_by_tag_collision(
            similar_artists
        )
    elif recommend_by == 'tracks':
        for track_name in tracks_names:
            recommended_artists += network.fetch_top_artists_by_track(
                track_name
            )
        recommended_artists = network.sort_artists_by_tag_collision(
            recommended_artists
        )
    elif recommend_by == 'tags':
        for tag_name in tags_names:
            recommended_artists += network.fetch_top_artists_by_tag(tag_name)
        recommended_artists = network.sort_artists_by_tag_collision(
            recommended_artists
        )

    for artist in recommended_artists:
        recommended_tracks += network.fetch_top_tracks_by_artist_name(
            artist_name=artist
        )

    return render(
        request,
        'results.html',
        context={
            'recommended_artists': recommended_artists[:artists_limit],
            'recommended_tracks': recommended_tracks[:tracks_limit],
        }
    )
