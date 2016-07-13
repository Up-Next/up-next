from django.shortcuts import render
from upnext.models import Track
from django.http import HttpResponse


def index(request):
    track_list = Track.objects
    context = {'track_list': track_list}
    return render(request, 'index.html', context)
