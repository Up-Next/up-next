import spotipy
import tokens
import re
from .models import Track


def cleanup_results(results):
    cleaned_results = []
    tracks = results['tracks']['items']

    for item in tracks:
        track = dict()
        track['song_title'] = item['name']
        track['artist'] = item['artists'][0]['name']
        track['uri'] = item['uri']
        track['preview'] = item['preview_url']
        track['album_image'] = item['album']['images'][1]['url']
        cleaned_results += [track]

    return cleaned_results


def add_to_playlist(track_info, party):
    token_info = tokens.token_read()

    # Adding on Spotify
    track_uri = re.search('uri\': u\'(.+?)\',', track_info).group(1)
    username = 'up--next'
    track_id = track_uri.split(':')[-1]
    party_id = party.uri.split(':')[-1]
    sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
    sp.user_playlist_add_tracks(username, party_id, [track_id])

    # Adding in DB
    track_artist = re.search('artist\': u\'(.+?)\'', track_info).group(1)
    track_title = re.search('song_title\': u(.+?), \'', track_info).group(1)
    track = Track(track_title=track_title, artist=track_artist, uri=track_uri, party=party)
    track.save()
