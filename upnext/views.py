from .forms import PartyForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import create_party
from refresh import Refresh
import spotipy
from .models import Party
import tracks
import scrape


has_been_called = False


@login_required
def create(request):
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            new_party = create_party.create_party_in_db(request, form)
            return redirect('successfully_created', party_url=new_party.url)
        else:
            return render(request, 'create.html', {'form': form})
    else:
        form = PartyForm()
        return render(request, 'create.html', {'form': form})


def index(request):
    print has_been_called, "has been called"

    if not has_been_called:
        refreshThread = Refresh()
        refreshThread.start()
        global has_been_called
        has_been_called = True

    if 'query' in request.GET:
        return party_search_results(request, request.GET['query'])

    user = request.user
    anon = user.is_anonymous()
    return render(request, 'index.html', {'anon': anon, 'redirect': False})


def login(request):
    return render(request, 'index.html', {'redirect': True, 'anon': True})


def party_detail(request, party_url):
    party_obj = Party.objects.get(url=party_url)
    party_tracks = party_obj.track_set.all()
    tracks_ordered = party_tracks.order_by('-score')
    party_embed_url = 'https://embed.spotify.com/?uri=' + party_obj.uri

    try:
        print "i got here"
        current = party_obj.track_set.get(current=True)
        print current
    except:
        current = None

    if request.user.username == party_obj.host and party_tracks:
        current = scrape.get_currently_playing(party_obj, party_embed_url)
        # print current, "current"

    if 'track_query' in request.GET:
        return track_search_results(request, request.GET['track_query'], party_obj)

    elif request.method == "POST":
        if 'track_up' in request.POST:
            tracks.upvote_track(request.POST['track_up'], party_obj)

        elif 'track_down' in request.POST:
            tracks.downvote_track(request.POST['track_down'], party_obj)

        elif 'new_host' in request.POST:
            party_obj.host = request.user.username
            party_obj.host_display = request.POST['display_name']
            party_obj.save()
    print current, "current before return"
    context = {'party': party_obj, 'tracks': tracks_ordered, 'current': current, 'embed': party_embed_url}
    return render(request, 'party_detail.html', context)


def track_search_results(request, query, party):
    if request.method == "POST":
        print request.POST, "request POST"
        tracks.add_to_playlist(request.POST['track_info'], party)
        return redirect('party_detail', party_url=party.url)

    sp = spotipy.Spotify()
    results = sp.search(query, limit=25)
    cleaned_results = tracks.cleanup_results(results)
    context = {'results': cleaned_results}
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
