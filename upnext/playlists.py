import tokens
import sys
import os
import spotipy
import spotipy.util as util

track_list = []
# be careful!!!
token_info = tokens.token_read()
sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])

