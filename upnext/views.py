from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render
from upnext.models import Track, Party
import requests


def index(request):
    track_list = Track.objects.all()
    context = {'track_list': track_list}
    return render(request, 'index.html', context)


def login(request):
    return HttpResponse("Welcome to UpNext! Please login to Spotify to continue.")


@login_required
def see_all_parties(request):
    parties = Party.objects.all()
    context = {'parties': parties}
    return render(request, 'see_all_parties.html', context)


def party(request, party_name):
    return HttpResponse("You're looking at party %s." % party_name)
