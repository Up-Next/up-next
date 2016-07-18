from __future__ import unicode_literals

from django.db import models


class Track(models.Model):
    track_title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='Unknown Artist')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.track_title


class Party(models.Model):
    party_name = models.CharField(max_length=200)

    def __str__(self):
        return self.party_name
