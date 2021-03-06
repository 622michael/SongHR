# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-23 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sfitbit', '0014_auto_20161122_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListenAudioSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_heart_rate', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('hr_loudness_correlation', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('hr_tempo_correlation', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='audiosegment',
            name='duration',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='listenaudiosegment',
            name='audio_segment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sfitbit.AudioSegment'),
        ),
        migrations.AddField(
            model_name='listenaudiosegment',
            name='listen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sfitbit.Listen'),
        ),
    ]
