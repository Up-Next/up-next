import spotipy
import tokens
from .models import Party


def create_party_in_db(request, form):
    new_party = form.save(commit=False)
    new_party.username = request.user.username
    new_party.save()
    create_playlist(request, new_party.party_name)
    return new_party


def create_playlist(request, party_name):
    username = 'up--next'
    user = request.user.social_auth.get(provider='spotify')
    print user.extra_data['access_token'], '\n\n\n', user.extra_data['refresh_token']
    token_info = tokens.token_read()
    token = token_info['ACCESS_TOKEN']
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlist = sp.user_playlist_create(username, party_name)
        party = Party.objects.get(party_name=party_name)
        party.uri = playlist['uri']
        party.save()
    else:
        print("Can't get token for", username)
