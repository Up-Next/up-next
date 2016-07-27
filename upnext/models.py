from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models


class Party(models.Model):
    party_allowed = RegexValidator(r'^[A-Za-z0-9-_ \'!]+$', 'Permitted characters: alphanumeric, space, -, _, \', !.')
    nickname_allowed = RegexValidator(r'^[A-Za-z ]+$', 'Permitted characters: alphabet, space.')

    party_name = models.CharField(max_length=100, validators=[party_allowed], default='', primary_key=True)
    user_nickname = models.CharField(max_length=80, validators=[nickname_allowed], default='')
    username = models.CharField(max_length=100, default='')
    uri = models.CharField(max_length=140, default='')
    url = models.CharField(max_length=140, default='', unique=True)
    created_at = models.DateTimeField(default='1995-07-12T13:20:30-08:00')

    def __str__(self):
        return self.party_name


class Track(models.Model):
    track_title = models.CharField(max_length=100, default='', primary_key=True)
    artist = models.CharField(max_length=100, default='')
    score = models.IntegerField(default=1)
    uri = models.CharField(max_length=140, default='')
    party = models.ForeignKey(Party, default=None)

    def __str__(self):
        return self.track_title + ", by " + self.artist
