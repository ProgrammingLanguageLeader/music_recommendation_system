import re
from django.shortcuts import render
from django.http import JsonResponse

from lastfm_api import LastfmNetwork


def index(request):
    return render(request, 'index.html')


def results(request):
    artists_limit = 20

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
    if recommend_by == 'artists':
        similar_artists = network.fetch_similar_artists(
            artists_names=artists_names,
            limit=artists_limit
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
    recommended_artists = [artist.name for artist in recommended_artists]

    data = {
        'isTaken': True,
        'recommendedArtists': recommended_artists[:artists_limit],
        'success': bool(recommended_artists),
    }
    return JsonResponse(data)
