import spotipy
from django.utils import timezone
import spotipy.util as util

def create_party_in_db(request, form):
    new_party = form.save(commit=False)
    new_party.username = request.user.username
    new_party.created_at = timezone.now()
    new_party.save()
    create_playlist(request, new_party.party_name)
    return new_party

def create_playlist(request, party_name):
  username = request.user.username
  user = request.user.social_auth.get(provider='spotify')
  token = user.extra_data['access_token']
  if token:
      sp = spotipy.Spotify(auth=token)
      sp.trace = False
      playlist = sp.user_playlist_create(username, party_name)
      print playlist, "playlist"
  else:
      print("Can't get token for", username)
