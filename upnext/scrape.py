from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from .models import Party, Track
import spotipy
import tokens


def get_currently_playing(party, embed):
  token_info = tokens.token_read()
  sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
  # playlist_url = get_playlist_url()
  party_id = party.uri.split(':')[-1]

  profile = webdriver.FirefoxProfile()
  profile.set_preference("webdriver.load.strategy", "unstable")
  browser = webdriver.Firefox(firefox_profile=profile)
  browser.get(embed)
  time.sleep(3)
  bond_source = browser.page_source
  browser.quit()
  track_in_db = None
  soup = BeautifulSoup(bond_source, "html.parser")
  results = soup.findAll("li", {"class": "track-row playing"})
  if results:
    now_playing = results[0]
    print now_playing
    current_track_uri = now_playing['data-uri']

    try:
      old_current_in_db = party.track_set.get(current=True)
    except:
      old_current_in_db = None

    if old_current_in_db and old_current_in_db.uri != current_track_uri:
      sp.user_playlist_remove_all_occurrences_of_tracks('up--next', party_id, [old_current_in_db.uri])
      old_current_in_db.current = False
      old_current_in_db.save()
      old_current_in_db.delete()

    track_in_db = party.track_set.get(uri=current_track_uri)
    track_in_db.current = True
    track_in_db.save()

  return track_in_db
