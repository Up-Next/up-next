# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 03:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('upnext', '0018_auto_20160722_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 23, 3, 30, 22, 113509, tzinfo=utc)),
        ),
    ]