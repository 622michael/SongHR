# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-16 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfitbit', '0006_auto_20161116_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='spotify_refresh_token',
            field=models.CharField(max_length=131, null=True),
        ),
    ]