import spotipy
from django.utils import timezone
import spotipy.util as util
from django.conf import settings
import tokens
from .models import Party


def create_party_in_db(request, form):
    new_party = form.save(commit=False)
    new_party.username = request.user.username
    new_party.created_at = timezone.now()
    new_party.save()
    create_playlist(request, new_party.party_name)
    return new_party

def create_playlist(request, party_name):
  username = 'up--next'
  user = request.user.social_auth.get(provider='spotify')
  token_info = tokens.token_read()
  token = token_info['ACCESS_TOKEN']
  refresh = token_info['REFRESH_TOKEN']
  if token:
      sp = spotipy.Spotify(auth=token)
      sp.trace = False
      playlist = sp.user_playlist_create(username, party_name)
      print playlist, "playlist"
      party = Party.objects.get(party_name=party_name)
      party.uri = playlist['uri']
      party.save()
      print party.uri, "uri"
  else:
      print("Can't get token for", username)
