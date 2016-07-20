from .forms import PartyForm
from django.utils import timezone
from upnext.models import Track, Party
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


def index(request):
    user = request.user
    anon = user.is_anonymous()
    context = {'anon': anon, 'redirect': False}
    return render(request, 'index.html', context)


def see_all_parties(request):
    parties = Party.objects.all()
    context = {'parties': parties}
    return render(request, 'see_all_parties.html', context)


def successfully_created(request, party):
    context = {'party': party}
    print type(party), "type"
    return render(request, 'successfully_created.html', context)


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
            # If data is invalid, this adds error messages.
            # Note: do not reset form
            return render(request, 'create.html', {'form': form})
    else:
        form = PartyForm()
        return render(request, 'create.html', {'form': form})


def login(request):
    context = {'redirect': True, 'anon': True}
    print request.path, "path"
    return render(request, 'index.html', context)


def party_detail(request, party):
    my_party = get_object_or_404(Party, pk=party)
    context = {'party': my_party}
    return render(request, 'party_detail.html', context)
