from .forms import PartyForm, ScoreForm
from .models import Party, Voter
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from refresh import Refresh
import create_party
import spotipy
import tracks
import re


has_been_called = False


def about(request):
    return render(request, 'about.html', {})


@login_required
def create(request):
    if request.method == 'POST':
        form = PartyForm(request.user, request.POST)
        if form.is_valid():
            new_party = create_party.create_party_in_db(request, form)
            return HttpResponseRedirect(reverse('successfully_created', args=(new_party.url,)))
        else:
            return render(request, 'create.html', {'form': form})
    else:
        form = PartyForm(request.user)
        return render(request, 'create.html', {'form': form})


def index(request):
    if not has_been_called:
        refreshThread = Refresh()
        refreshThread.start()
        global has_been_called
        has_been_called = True

    if 'query' in request.GET:
        return party_search_results(request, request.GET['query'])

    user = request.user
    anon = user.is_anonymous()
    admin = user.is_staff

    if not anon:
        if not Voter.objects.exists():
            current_voter = Voter(username=request.user.username)
            current_voter.save()
        elif Voter.objects.last().username != request.user.username:
            current_voter, _ = Voter.objects.get_or_create(username=request.user.username)
            current_voter.save()

    return render(request, 'index.html', {'anon': anon, 'redirect': False, 'admin': admin})


def login(request):
    return render(request, 'index.html', {'redirect': True, 'anon': True})


@login_required
def party_detail(request, party_url):
    party_obj = Party.objects.get(url=party_url)
    party_tracks = party_obj.track_set.all()
    tracks_ordered = party_tracks.order_by('-score', 'track_title', 'artist')
    voter = Voter.objects.get(username=request.user.username)
    form = ScoreForm()
    if 'track_query' in request.GET:
        return track_search_results(request, request.GET['track_query'], party_obj)

    elif request.method == 'POST':
        if 'track_up' in request.POST:
            tracks.upvote_track(request.POST['track_up'], party_obj, request.user.username)
        elif 'track_down' in request.POST:
            tracks.downvote_track(request.POST['track_down'], party_obj, request.user.username)
        elif 'remove' in request.POST:
            track_info = request.POST['remove']
            track_title = re.search('^(.+?), by', track_info).group(1)
            track_artist = re.search('by (.+?)$', track_info).group(1)
            track = party_obj.track_set.get(track_title=track_title, artist=track_artist)
            tracks.remove_from_playlist(track, party_obj)
        elif 'min_score' in request.POST:
            form = ScoreForm(request.POST)
            if form.is_valid():
                party_obj.min_score = request.POST['min_score']
                party_obj.save()
                tracks.remove_min_score(party_obj)
        return HttpResponseRedirect(reverse('party_detail', args=(party_url,)))

    context = {'party': party_obj, 'tracks': tracks_ordered, 'down': voter.down_tracks.all(), 'up': voter.up_tracks.all(), 'current_user': request.user.username, 'form': form}


    return render(request, 'party_detail.html', context)


@login_required
def track_search_results(request, query, party):
    if request.method == 'POST':
        tracks.add_to_playlist(request.POST['track_uri'], party, request.user.username)
        return HttpResponseRedirect(reverse('party_detail', args=(party.url,)))

    sp = spotipy.Spotify()
    results = sp.search(query, limit=25)
    cleaned_results = tracks.cleanup_results(results)
    context = {'results': cleaned_results, 'party': party}
    return render(request, 'track_search_results.html', context)


def party_search_results(request, query):
    results = Party.objects.filter(party_name__icontains=query)
    return render(request, 'party_search_results.html', {'results': results})


def see_all_parties(request):
    parties = Party.objects.all()
    return render(request, 'see_all_parties.html', {'parties': parties})


def successfully_created(request, party_url):
    party_obj = Party.objects.get(url=party_url)
    return render(request, 'successfully_created.html', {'party': party_obj})
