from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Party(models.Model):
    party_allowed = RegexValidator(r'^[A-Za-z0-9-_]+$', 'Permitted characters: alphanumeric, dash, underscore.')
    nickname_allowed = RegexValidator(r'^[A-Za-z]+$', 'Permitted characters: alphabet.')

    party_name = models.CharField(max_length=140, validators=[party_allowed], default='', primary_key=True)
    user_nickname = models.CharField(max_length=100, validators=[nickname_allowed], default='')
    username = models.CharField(max_length=200, default='No Username')
    created_at = models.DateTimeField(default=timezone.now())
    uri = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.party_name


class Track(models.Model):
    track_title = models.CharField(max_length=200, default='Unnamed Track')
    artist = models.CharField(max_length=200, default='Unknown Artist')
    score = models.IntegerField(default=0)
    uri = models.CharField(max_length=200, default='')
    party = models.ForeignKey(Party, default=0)

    def __str__(self):
        return self.track_title + ", by " + self.artist
