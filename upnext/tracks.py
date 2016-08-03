import spotipy
import tokens
import re
import unicodedata
from .models import Track, Voter


def cleanup_results(results):
    cleaned_results = []
    tracks = results['tracks']['items']

    for item in tracks:
        track = cleanup_one(item)
        cleaned_results += [track]

    return cleaned_results


def cleanup_one(track_item):
    track = dict()
    track['song_title'] = track_item['name']
    track['artist'] = track_item['artists'][0]['name']
    track['uri'] = track_item['uri']
    track['preview'] = track_item['preview_url']
    track['album_image'] = track_item['album']['images'][1]['url']
    return track


def add_to_playlist(track_uri, party):
    token_info = tokens.token_read()

    # Adding on Spotify
    if party.track_set.filter(uri=track_uri).exists():
        print "Can't add duplicate track"
        return

    username = 'up--next'
    track_id = track_uri.split(':')[-1]
    party_id = party.uri.split(':')[-1]
    sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
    sp.user_playlist_add_tracks(username, party_id, [track_id])

    track_item = sp.track(track_id)
    track_info = cleanup_one(track_item)

    # Adding in DB
    track_artist = unicodedata.normalize('NFKD', track_info['artist']).encode('ascii', 'ignore')
    track_title = unicodedata.normalize('NFKD', track_info['song_title']).encode('ascii', 'ignore')

    track = Track(track_title=track_title, artist=track_artist, uri=track_uri, party=party)
    track.save()

    old_position = len(party.track_set.all()) - 1

    ordered = party.track_set.order_by('-score')
    new_position = get_index(track, ordered)

    reorder_playlist(party, old_position, new_position)


def upvote_track(track_info, party, voter_name):
    track_title = re.search('^(.+?), by', track_info).group(1)
    track_artist = re.search('by (.+?)$', track_info).group(1)
    up_track = party.track_set.get(track_title=track_title, artist=track_artist)

    voter = Voter.objects.get(username=voter_name)

    # Ensure voter hasn't already upvoted
    if not voter.up_tracks.filter(track_title=track_title, artist=track_artist, party=party).exists():

        ordered_old = party.track_set.order_by('-score')
        old_position = get_index(up_track, ordered_old)

        up_track.score += 1

        # If voter has previously downvoted, upvote one more to fix
        if voter.down_tracks.filter(track_title=track_title, artist=track_artist, party=party).exists():
            up_track.score += 1
            voter.down_tracks.remove(up_track)

        up_track.save()
        voter.up_tracks.add(up_track)

        ordered_new = party.track_set.order_by('-score')
        new_position = get_index(up_track, ordered_new)

        reorder_playlist(party, old_position, new_position)
        
    else:
        print "Undoing upvote"
        undo_vote(up_track, party, voter, 'up')


def downvote_track(track_info, party, voter_name):
    track_title = re.search('^(.+?), by', track_info).group(1)
    track_artist = re.search('by (.+?)$', track_info).group(1)
    down_track = party.track_set.get(track_title=track_title, artist=track_artist)

    voter = Voter.objects.get(username=voter_name)

    # Ensure voter hasn't already downvoted
    if not voter.down_tracks.filter(track_title=track_title, artist=track_artist, party=party).exists():

        ordered_old = party.track_set.order_by('-score')
        old_position = get_index(down_track, ordered_old)

        down_track.score -= 1

        # If voter has previously upvoted, downvote one more to fix
        if voter.up_tracks.filter(track_title=track_title, artist=track_artist, party=party).exists():
            down_track.score -= 1
            voter.up_tracks.remove(down_track)

        down_track.save()
        voter.down_tracks.add(down_track)

        ordered_new = party.track_set.order_by('-score')
        new_position = get_index(down_track, ordered_new)

        reorder_playlist(party, old_position, new_position)

        if down_track.score <= party.min_score:
            remove_from_playlist(down_track, party)

    else:
        print "Undoing downvote"
        undo_vote(down_track, party, voter, 'down')


def reorder_playlist(party, old_position, new_position):
    token_info = tokens.token_read()

    party_id = party.uri.split(':')[-1]

    sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
    sp.user_playlist_reorder_tracks('up--next', party_id, old_position, new_position)


def remove_from_playlist(track, party):
    # Remove from Spotify
    token_info = tokens.token_read()

    username = 'up--next'
    track_id = track.uri.split(':')[-1]
    party_id = party.uri.split(':')[-1]

    sp = spotipy.Spotify(auth=token_info['ACCESS_TOKEN'])
    sp.user_playlist_remove_all_occurrences_of_tracks(username, party_id, [track_id])

    # Remove from DB
    party.track_set.get(uri=track.uri).delete()


def undo_vote(track, party, voter, up_or_down):
    ordered_old = party.track_set.order_by('-score')
    old_position = get_index(track, ordered_old)

    if up_or_down == 'up':
        track.score -= 1
        voter.up_tracks.remove(track)
    elif up_or_down == 'down':
        track.score += 1
        voter.down_tracks.remove(track)

    track.save()

    ordered_new = party.track_set.order_by('-score')
    new_position = get_index(track, ordered_new)

    reorder_playlist(party, old_position, new_position)


def get_index(track, track_list):
    for index, item in enumerate(track_list):
        if track == item:
            return index


def get_uri(track_info):
    try:
        return re.search('uri\': u\'(.+?)\',', track_info).group(1)
    except AttributeError:
        print "Track URI not found"


def get_artist(track_info):
    try:
        return re.search('artist\': u\"(.+?)\"', track_info).group(1)
    except AttributeError:
        try:
            return re.search('artist\': u\'(.+?)\'', track_info).group(1)
        except AttributeError:
            print "Track artist not found"


def get_title(track_info):
    try:
        return re.search('song_title\': u(.+?), \'', track_info).group(1)
    except AttributeError:
        print "Track title not found"
