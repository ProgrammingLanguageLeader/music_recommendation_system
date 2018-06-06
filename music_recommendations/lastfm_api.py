from collections import defaultdict
import pylast
import math

from .config import Config


class LastfmNetwork:
    def __init__(self):
        self.network = pylast.LastFMNetwork(
            api_secret=Config.API_SECRET,
            api_key=Config.API_KEY
        )

    def fetch_similar_artists(self, artists_names, limit=10):
        artists = [
            self.network.get_artist(artist_name)
            for artist_name in artists_names
        ]
        similar_artists = []

        for artist in artists:
            similar_to_single_artist = artist.get_similar(limit=limit)
            if similar_to_single_artist:
                similar_artists += [
                    artist.item
                    for artist in similar_to_single_artist
                ]
                continue
            top_tags = [
                tag.item
                for tag in artist.get_top_tags(limit=5)
            ]
            similar_to_single_artist = []
            tag_limit = math.ceil(limit / 5)
            for tag in top_tags:
                similar_to_single_artist += tag.get_top_artists(
                    limit=tag_limit
                )
            similar_artists += [
                artist.item
                for artist in similar_to_single_artist
            ]
        return similar_artists

    @staticmethod
    def sort_artists_by_tag_collision(artists):
        artist_tags = defaultdict(list)
        for artist in artists:
            tags = artist.get_top_tags(limit=5)
            for tag in tags:
                artist_tags[tag].append(artist)
        sorted_artists = []
        artist_tags = sorted(
            artist_tags.items(),
            key=lambda key_value: len(key_value[1]),
            reverse=True
        )
        for tag, artists in artist_tags:
            for artist in artists:
                if artist not in sorted_artists:
                    sorted_artists.append(artist)
        return sorted_artists

    def fetch_top_tracks_by_artist_name(self, artist_name, count=3):
        artist = self.network.get_artist(artist_name)
        tracks = artist.get_top_tracks(limit=count)
        return [str(track.item) for track in tracks]

    def fetch_top_artists_by_tag(self, tag_name, limit=10):
        tag = self.network.get_tag(tag_name)
        top_artists = tag.get_top_artists(limit=limit)
        return [
            artist.item
            for artist in top_artists
        ]

    def fetch_top_artists_by_track(self, track_name, limit=10):
        track_artist, track_title = track_name.split('-')
        track_artist = track_artist.strip()
        track_title = track_title.strip()
        track = self.network.get_track(track_artist, track_title)
        top_tags = track.get_top_tags()[:5]
        if not top_tags:
            top_tags = track.get_artist().get_top_tags()[:5]
        top_artists = []
        for tag in top_tags:
            top_artists += self.fetch_top_artists_by_tag(
                tag_name=tag.item,
                limit=limit
            )
        return top_artists
