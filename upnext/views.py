from .forms import PartyForm
from django.utils import timezone
from upnext.models import Party
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            new_party = form.save(commit=False)
            new_party.username = request.user.username
            new_party.created_at = timezone.now()
            new_party.save()
            return successfully_created(request, new_party)
        else:
            return render(request, 'create.html', {'form': form})
    else:
        form = PartyForm()
        return render(request, 'create.html', {'form': form})


def index(request):
    if 'query' in request.GET:
        return search_results(request, request.GET['query'])

    user = request.user
    anon = user.is_anonymous()
    return render(request, 'index.html', {'anon': anon, 'redirect': False})


def login(request):
    return render(request, 'index.html', {'redirect': True, 'anon': True})


def party_detail(request, party):
    my_party = get_object_or_404(Party, pk=party)
    return render(request, 'party_detail.html', {'party': my_party})


def search_results(request, query):
    results = Party.objects.filter(party_name__icontains=query)
    return render(request, 'search_results.html', {'results': results})


def see_all_parties(request):
    parties = Party.objects.all()
    return render(request, 'see_all_parties.html', {'parties': parties})


def successfully_created(request, party):
    return render(request, 'successfully_created.html', {'party': party})
