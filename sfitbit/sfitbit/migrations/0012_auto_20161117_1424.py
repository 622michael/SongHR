# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-17 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfitbit', '0011_listen_average_heart_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listen',
            name='end',
            field=models.DateTimeField(null=True),
        ),
    ]
