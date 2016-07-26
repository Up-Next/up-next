import spotipy
import tokens
import re
from .models import Track


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
        cleaned_results += [track]

    return cleaned_results


def add_to_playlist(track_info, party):
    token_info = tokens.token_read()

    # Adding on Spotify
    try:
        track_uri = re.search('uri\': u\'(.+?)\',', track_info).group(1)
    except AttributeError:
        print "Track URI not found"

    username = 'up--next'
    track_id = track_uri.split(':')[-1]
    party_id = party.uri.split(':')[-1]
    sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
    sp.user_playlist_add_tracks(username, party_id, [track_id])

    # Adding in DB
    try:
        track_artist = re.search('artist\': u\'(.+?)\'', track_info).group(1)
    except AttributeError:
        print "Track artist not found"

    try:
        track_title = re.search('song_title\': u(.+?), \'', track_info).group(1)
    except AttributeError:
        print "Track title not found"

    track = Track(track_title=track_title, artist=track_artist, uri=track_uri, party=party)
    track.save()

    old_position = len(party.track_set.all()) - 1

    ordered = party.track_set.order_by('-score')
    new_position = get_index(track, ordered)

    reorder_playlist(party, old_position, new_position)


def upvote_track(track_info, party):
    track_title = re.search('^(.+?), by', track_info).group(1)
    up_track = party.track_set.get(track_title=track_title)

    ordered_old = party.track_set.order_by('-score')
    old_position = get_index(up_track, ordered_old)

    up_track.score += 1
    up_track.save()

    ordered_new = party.track_set.order_by('-score')
    new_position = get_index(up_track, ordered_new)

    reorder_playlist(party, old_position, new_position)


def downvote_track(track_info, party):
    track_title = re.search('^(.+?), by', track_info).group(1)
    down_track = party.track_set.get(track_title=track_title)

    ordered_old = party.track_set.order_by('-score')
    old_position = get_index(down_track, ordered_old)

    down_track.score -= 1
    down_track.save()

    ordered_new = party.track_set.order_by('-score')
    new_position = get_index(down_track, ordered_new)

    reorder_playlist(party, old_position, new_position)


def reorder_playlist(party, old_position, new_position):
    token_info = tokens.token_read()

    party_id = party.uri.split(':')[-1]

    sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
    sp.user_playlist_reorder_tracks('up--next', party_id, old_position, new_position)


def get_index(track, track_list):
    for index, item in enumerate(track_list):
        if track == item:
            return index
