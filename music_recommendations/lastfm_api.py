import pylast

from config import Config


class LastfmNetwork:
    def __init__(self):
        self.network = pylast.LastFMNetwork(
            api_secret=Config.API_SECRET,
            api_key=Config.API_KEY
        )

    def get_similar_artists(self, artist_name, count=10):
        artist_obj = self.network.get_artist(artist_name)

        similar_artists = artist_obj.get_similar(limit=count)
        if similar_artists:
            similar_artists = [
                str(artist.item)
                for artist in similar_artists
            ]
            return similar_artists

        top_tags = [
            tag.item
            for tag in artist_obj.get_top_tags(limit=3)
        ]
        top_artists = []
        for tag_obj in top_tags:
            top_artists += tag_obj.get_top_artists(limit=count // 3)

        similar_artists = [
            str(artist_obj.item)
            for artist_obj in top_artists
        ]
        return similar_artists

    def get_top_tracks_by_artist(self, artist_name, count=3):
        artist = self.network.get_artist(artist_name)
        tracks = artist.get_top_tracks(limit=count)
        return [str(track.item) for track in tracks]


if __name__ == '__main__':
    a = LastfmNetwork()
    # s = a.get_similar_artists('System of a down')
    # print(s)
    s = a.get_similar_artists('Lil Peep')
    print(s)
    print(a.get_top_tracks_by_artist('Самое большое простое число'))
