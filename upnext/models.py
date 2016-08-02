from __future__ import unicode_literals
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models


class Party(models.Model):
    party_allowed = RegexValidator(r'^[A-Za-z0-9-_ \'!]+$', 'Permitted party name characters: alphanumeric, space, -, _, \', !.')
    nickname_allowed = RegexValidator(r'^[A-Za-z ]+$', 'Permitted user nickname characters: alphabet, space.')
    url_allowed = RegexValidator(r'^[A-za-z0-9-]+$', 'Permitted URL characters: alphanumeric, dashes.')

    party_name = models.CharField(max_length=100, validators=[party_allowed], default='', primary_key=True)
    user_nickname = models.CharField(max_length=80, validators=[nickname_allowed], default='')
    url = models.CharField(max_length=140, validators=[url_allowed], default='', unique=True)
    username = models.CharField(max_length=100, default='')
    uri = models.CharField(max_length=140, default='')
    min_score = models.IntegerField(default=-10, validators=[MaxValueValidator(-1)])
    created_at = models.DateTimeField(default='1995-07-12T13:20:30-08:00')

    def __str__(self):
        return self.party_name


class Track(models.Model):
    track_title = models.CharField(max_length=100, default='')
    artist = models.CharField(max_length=100, default='')
    score = models.IntegerField(default=0)
    uri = models.CharField(max_length=140, default='')
    party = models.ForeignKey(Party, default=None)

    def __str__(self):
        return self.track_title + ", by " + self.artist


class Voter(models.Model):
    username = models.CharField(max_length=100, default='', unique=True)
    up_tracks = models.ManyToManyField(Track, related_name='upvoted')
    down_tracks = models.ManyToManyField(Track, related_name='downvoted')

    def __str__(self):
        return "Spotify username: " + self.username
