# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upnext', '0003_party_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='host_display',
            field=models.CharField(default='', max_length=100),
        ),
    ]
