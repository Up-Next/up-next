import sys
import os
import spotipy
import spotipy.util as util
import tokens


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
    cleaned_results+= [track]

  print len(cleaned_results)
  return cleaned_results


def add_to_playlist(track_uri, party):
  token_info = tokens.token_read()

  username = 'up--next'
  track_id = track_uri.split(':')[-1]
  print track_id
  party_id = party.uri.split(':')[-1]
  sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
  results = sp.user_playlist_add_tracks(username, party_id, [track_id])
  print results

