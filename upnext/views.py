from django.shortcuts import render
from upnext.models import Track
from django.http import HttpResponse


def index(request):
    track_list = Track.objects
    context = {'track_list': track_list}
    return render(request, 'index.html', context)


def login(request):
    return HttpResponse("Welcome to UpNext! Please login to Spotify to continue.")


def find_or_create_party(request):
    return HttpResponse("Type a party name to find a party, or create a new party.")


def party(request, party_name):
    return HttpResponse("You're looking at party %s." % party_name)
