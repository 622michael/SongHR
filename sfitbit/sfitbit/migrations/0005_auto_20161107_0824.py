# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-07 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfitbit', '0004_auto_20161107_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='listen',
            name='ended',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='listen',
            name='end',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
