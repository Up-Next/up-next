from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# def get_playlist_url():


def get_currently_playing():
  # playlist_url = get_playlist_url()
  current_track = dict()

  profile = webdriver.FirefoxProfile()
  profile.set_preference("webdriver.load.strategy", "unstable")
  browser = webdriver.Firefox(firefox_profile=profile)
  browser.get('https://embed.spotify.com/?uri=spotify%3Auser%3Aup--next%3Aplaylist%3A3JiPzv7ACiVk7ap6mowN71')
  time.sleep(3)
  bond_source = browser.page_source
  browser.quit()

  soup = BeautifulSoup(bond_source, "html.parser")
  now_playing = soup.findAll("li", {"class": "track-row playing"})[0]
  print now_playing
  song_title = now_playing['data-name']
  current_track['artist'] = now_playing['data-artists']

  current_track['title'] = now_playing['data-name']

  current_track['uri'] = now_playing['data-uri']

  current_track['position'] = now_playing['data-position']


  print current_track
  return current_track
