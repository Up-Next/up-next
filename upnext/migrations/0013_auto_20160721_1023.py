# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 17:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('upnext', '0012_auto_20160721_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 21, 17, 23, 57, 913147, tzinfo=utc)),
        ),
    ]