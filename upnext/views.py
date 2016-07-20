from .forms import PartyForm
from django.utils import timezone
from upnext.models import Track, Party
from django.shortcuts import render


def index(request):
    user = request.user
    anon = user.is_anonymous()
    context = {'anon': anon}
    return render(request, 'index.html', context)


def see_all_parties(request):
    parties = Party.objects.all()
    context = {'parties': parties}
    return render(request, 'see_all_parties.html', context)


def successfully_created(request):
    return render(request, 'successfully_created.html', {})


def create(request):
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            new_party = form.save(commit=False)
            new_party.username = request.user
            new_party.created_at = timezone.now()
            new_party.save()
            return render(request, 'successfully_created.html', {'form': form})
        else:
            # If data is invalid, this adds error messages.
            # Note: do no reset form
            return render(request, 'create.html', {'form': form})
    else:
        form = PartyForm()
        return render(request, 'create.html', {'form': form})
