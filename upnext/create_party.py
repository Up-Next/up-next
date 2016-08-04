import spotipy
import tokens
from .models import Party, Track
from django.utils import timezone
import unicodedata
import spotipy.oauth2 as oauth2
from django.conf import settings


def create_party_in_db(request, form):
    new_party = form.save(commit=False)
    new_party.username = request.user.username
    new_party.save()
    create_playlist(request, new_party)
    return new_party


def create_playlist(request, party):
    username = 'up--next'
    user = request.user.social_auth.get(provider='spotify')
    token_info = tokens.token_read()
    token = token_info['ACCESS_TOKEN']

    if token:
        sp_admin = spotipy.Spotify(auth=token)
        sp_oauth = oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID,
                                       settings.SPOTIPY_CLIENT_SECRET,
                                       settings.SPOTIPY_REDIRECT_URI,
                                       scope=settings.SOCIAL_AUTH_SPOTIFY_SCOPE[0])
        new_token_info = sp_oauth._refresh_access_token(user.extra_data['refresh_token'])
        sp_user = spotipy.Spotify(auth=new_token_info['access_token'])
        sp_user.trace = False

        playlist = sp_admin.user_playlist_create(username, party.party_name)

        initial_uri = party.uri
        party.uri = playlist['uri']
        party.created_at = timezone.now()
        party.save()

        # Load songs from initial playlist into new playlist
        if initial_uri != "UpNext - Start a new playlist":
            load_from_playlist(initial_uri, party, sp_user, request.user.username, user, token_info['ACCESS_TOKEN'])

    else:
        print("Can't get token for", username)


def load_from_playlist(playlist_uri, party, client, added_by, user_auth, token):
    tracks_info = client.user_playlist_tracks(user_auth, playlist_id=playlist_uri)['items']
    track_uris = [item['track']['uri'] if 'local' not in item else 'local' for item in tracks_info]
    track_titles = [item['track']['name'] for item in tracks_info]
    artists = [item['track']['artists'][0]['name'] for item in tracks_info]

    for i in xrange(len(track_uris)):

        if track_uris[i] != 'local':

            if not party.track_set.filter(uri=track_uris[i]).exists():
                # Add all the tracks to the DB
                track_artist = unicodedata.normalize('NFKD', artists[i]).encode('ascii', 'ignore')
                track_title = unicodedata.normalize('NFKD', track_titles[i]).encode('ascii', 'ignore')
                track = Track(track_title=track_title,
                              artist=track_artist,
                              uri=track_uris[i],
                              party=party,
                              added_by=added_by)
                track.save()

    # Add all the tracks to Spotify in order
    username = 'up--next'
    party_id = party.uri.split(':')[-1]

    ordered_tracks = party.track_set.order_by('-score', 'track_title', 'artist')
    track_ids = [item.uri.split(':')[-1] for item in ordered_tracks]

    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_add_tracks(username, party_id, track_ids)
