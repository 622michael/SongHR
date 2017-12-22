# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-23 03:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sfitbit', '0013_heartrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DecimalField(decimal_places=5, max_digits=10, null=True)),
                ('tempo', models.DecimalField(decimal_places=5, max_digits=10, null=True)),
                ('loudness', models.DecimalField(decimal_places=5, max_digits=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='track',
            name='duration',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='loudness',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='audiosegment',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sfitbit.Track'),
        ),
    ]