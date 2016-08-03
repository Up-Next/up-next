import spotipy
import tokens
from .models import Party, Track
from django.utils import timezone
import tracks
import spotipy.oauth2 as oauth2
from django.conf import settings



def create_party_in_db(request, form):
    new_party = form.save(commit=False)
    new_party.username = request.user.username
    new_party.save()
    create_playlist(request, new_party.party_name)
    return new_party


def create_playlist(request, party_name):
    username = 'up--next'
    user = request.user.social_auth.get(provider='spotify')
    print "helloooooo"
    token_info = tokens.token_read()
    token = token_info['ACCESS_TOKEN']
    if token:
        sp_oauth = oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID,
                                       settings.SPOTIPY_CLIENT_SECRET,
                                       settings.SPOTIPY_REDIRECT_URI,
                                       scope=settings.SOCIAL_AUTH_SPOTIFY_SCOPE[0])
        new_token_info = sp_oauth._refresh_access_token(user.extra_data['refresh_token'])
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlist = sp.user_playlist_create(username, party_name)
        party = Party.objects.get(party_name=party_name)
        initial_uri = party.uri
        party.uri = playlist['uri']
        party.created_at = timezone.now()
        party.save()

        # Load songs from initial playlist into new playlist
        if initial_uri != "UpNext - Start a new playlist":
            tracks_info = sp.user_playlist_tracks(user, playlist_id=initial_uri)["items"]
            uris = map(lambda x: x["track"]["uri"].split(":")[-1], tracks_info)
            track_titles = map(lambda x: x["track"]["name"], tracks_info)
            artists = map(lambda x: x["track"]["artists"][0]["name"], tracks_info)
            for i in range(len(uris)):
                if not party.track_set.filter(uri=uris[i]).exists():
                    sp.user_playlist_add_tracks(username, party.uri, [uris[i]])
                    track = Track(track_title=track_titles[i], artist=artists[i], uri=uris[i], party=party)
                    track.save()

    else:
        print("Can't get token for", username)
