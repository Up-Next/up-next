from .forms import PartyForm
from django.utils import timezone
from upnext.models import Party
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import create_party
import requests
from refresh import Refresh
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import pprint
from .models import Party
import tracks


has_been_called = False


@login_required
def create(request):
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            new_party = create_party.create_party_in_db(request, form)
            return redirect('successfully_created', party=new_party)
            # return successfully_created(request, new_party)
        else:
            return render(request, 'create.html', {'form': form})
    else:
        form = PartyForm()
        return render(request, 'create.html', {'form': form})


def index(request):
    print has_been_called, "has it"
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


def party_detail(request, party):
    my_party = get_object_or_404(Party, pk=party)
    party_obj = Party.objects.get(party_name = party)
    if 'track_query' in request.GET:
        return track_search_results(request, request.GET['track_query'], party_obj)
    print party_obj.party_name, "name", party_obj.uri, "uri"
    return render(request, 'party_detail.html', {'party': party_obj})


def track_search_results(request, query, party):
    if request.method == "POST":
        print request.POST, "hello"
        tracks.add_to_playlist(request.POST['track_uri'], party)
    sp = spotipy.Spotify()
    print sp
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


def successfully_created(request, party):
    return render(request, 'successfully_created.html', {'party': party})
