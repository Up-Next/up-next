import spotipy
from django.conf import settings
import time
from threading import Thread
import spotipy.util as util
import spotipy.oauth2 as oauth2
import tokens


class Refresh(Thread):
  def refresh_tokens(self):
    username = 'up--next'
    sp_oauth = oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID,
      settings.SPOTIPY_CLIENT_SECRET,
      settings.SPOTIPY_REDIRECT_URI,
      scope = settings.SOCIAL_AUTH_SPOTIFY_SCOPE[0]
      )
    saved_tokens = tokens.token_read()
    token_info = sp_oauth._refresh_access_token(saved_tokens['REFRESH_TOKEN'])
    tokens.token_write(token_info['access_token'], token_info['refresh_token'])

  def refresh(self):
    print "I refreshed"
    while True:
      self.refresh_tokens()
      time.sleep(60 * 50)

  def run(self):
    self.refresh()
