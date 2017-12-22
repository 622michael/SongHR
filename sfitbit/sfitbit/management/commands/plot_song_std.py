from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, ListenAudioSegment, AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from sfitbit import fitbit, audio, heart_rates
from datetime import datetime, timedelta, time
import pytz
from sfitbit import spotify
import random

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '--id',
            action='store',
            dest='track_id',
            default=None,
            help='Display graph for a specific song' )
		parser.add_argument(
        	'--random', 
        	action = 'store',
        	dest = 'random',
        	default = False, 
        	help = 'Display graphs in random order'
       	)

	def handle(self, *args, **options):

		if options["track_id"] is not None:
			try:
				tracks = [Track.objects.get(id = options["track_id"])]
			except:
				print "invaid id"
				return 
		else:
			tracks = Track.objects.all()
			if options["random"]:
				tracks = tracks[:len(tracks)]
				tracks = sorted(tracks, key=lambda x: random.random())


		colors = ('r', 'c', 'm', 'y', 'k')
		color_index = 0

		for track in tracks:
			if len(Listen.objects.filter(track = track)) < 4:
				continue

			# tempos, loudness, times = audio.tempo_loudness_time_arrays(track, tempo_offset = -60, loudness_offset = 60)
			# plt.plot(times, tempos, "b")
			# plt.plot(times, loudness, "g")


			for listen in Listen.objects.filter(track = track):
				if (listen.end - listen.start).total_seconds() > float(track.duration) + 60.0:
					continue 	
				hrs = np.array([])
				times = []
				for sec in range (0, int((listen.end - listen.start).total_seconds())):
					hr = heart_rates.heart_rate_at_time(listen, sec)
					if hr is None:
						continue

					hr = float(hr.value)
					hrs = np.append(hrs, hr)
					print "Heart rate at %i: %f" % (sec, hr)
					times.append(sec)


				hrs_mean = np.mean(hrs)
				print hrs_mean
				hrs_std = np.std(hrs)
				print hrs_std

				cache = {}
				hrs_zs = []
				for hr in hrs:
					try:
						hr_z = cache["%i" % hr]
					except KeyError:
						hr_z = (hr - hrs_mean)/hrs_std
						cache["%i" % hr] = hr_z

					print "%i : %f" % (hr, hr_z)
					hrs_zs.append(hr_z)

				print len(times)
				print len(hrs_zs)

				plt.plot(times, hrs_zs, colors[color_index], label = listen.id)

				color_index += 1
				if color_index == len(colors):
					color_index = 0

			plt.title(track.name)
			plt.title(track.id, loc='right')
			plt.show()