from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track
import matplotlib.pyplot as plt
import numpy as np
from sfitbit import fitbit
from datetime import datetime, timedelta, time
import pytz
from sfitbit import spotify, audio, heart_rates
import random

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '--id',
            action='store',
            dest='listen_id',
            default=None,
            help='Display graph for a specific song',
        )

		parser.add_argument(
            '--random',
            action='store',
            dest='random',
            default= False,
            help='Choose the next graph randomly'
        )
        # parser.add_argument(
        # 	'--no-title',
        # 	action = 'store',
        # 	dest = 'no_title',
        # 	default = False,
        # 	help = 'Display the title on the graph or not'
        # )

	def handle(self, *args, **options):
		if options["listen_id"] is not None:
			try:
				listens = Listen.objects.filter(id__gte = options["listen_id"])
			except:
				print "invaid id"
				return 
		else:
			listens = Listen.objects.all().order_by('id')
			
			if options["random"]:
				listens = listens[:len(listens)]
				listens = sorted(listens, key=lambda x: random.random())


		for listen in listens:
			if listen.track is None:
				print "run 'python manage.py connect_track_to_listen' to insure all listens have a track."
				continue

			track = listen.track 
		
			if (listen.end - listen.start).total_seconds() > float(track.duration) + 60.0:
					print "Listen substiantial longer than song"
					continue
			if(len(heart_rates.heart_rates_in_listen(listen)) < 3):
				print "Minimum heartrate data"
				continue
			
			average_heartrate = heart_rates.average_heart_rate(listen)

			tempo_offset = average_heartrate - float(listen.track.tempo)
			loudness_offset = average_heartrate - float(listen.track.loudness)
			tempos, loudnesses, times = audio.tempo_loudness_time_arrays(listen.track, 
				tempo_offset = tempo_offset, loudness_offset = loudness_offset)
			plt.plot(times, tempos, "b")
			plt.plot(times, loudnesses, "g")

			heartrates, times = heart_rates.heart_rate_time_arrays(listen)
			plt.plot(times, heartrates, "r")


			# if not options["no_title"]:
			plt.title(track.name + "T")
			plt.title(track.id, loc='right')
			plt.title(listen.id, loc='left')

			plt.show()
