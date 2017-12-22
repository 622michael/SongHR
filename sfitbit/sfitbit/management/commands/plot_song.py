from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, ListenAudioSegment, AudioSegment
import matplotlib.pyplot as plt
from sfitbit import fitbit, audio, heart_rates
from datetime import datetime, timedelta, time
import pytz
from sfitbit import spotify
import random

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '-id',
            action='store',
            dest='track_id',
            default=None,
            help='Display graph for a specific song',
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

		colors = ('r', 'c', 'm', 'y', 'k')
		color_index = 0

		for track in tracks:
			if len(Listen.objects.filter(track = track)) < 2:
				continue

			# tempos, loudness, times = audio.tempo_loudness_time_arrays(track, tempo_offset = -60, loudness_offset = 60)
			# plt.plot(times, tempos, "b")
			# plt.plot(times, loudness, "g")


			for listen in Listen.objects.filter(track = track):
				if (listen.end - listen.start).total_seconds() > float(track.duration) + 60.0:
					continue 

				heartrates, times = heart_rates.heart_rate_time_arrays(listen)
				plt.plot(times, heartrates, colors[color_index])

				# l_correlations, t_correlations, times = [], [], []

				# for audio_segment in AudioSegment.objects.filter(track = track):
				# 	try:
				# 		l_a_segment = ListenAudioSegment.objects.get(audio_segment = audio_segment, listen = listen)
				# 	except:
				# 		continue

				# 	l_correlations.append(abs(float(l_a_segment.hr_loudness_correlation))* 30.0 + 30.0)
				# 	t_correlations.append(abs(float(l_a_segment.hr_tempo_correlation)) + 60)
				# 	times.append(audio_segment.time)
				# 	plt.plot(times, l_correlations, colors[color_index] + "o")
				# 	plt.plot(times, t_correlations, colors[color_index] + "+")


				color_index += 1
				if color_index == len(colors):
					color_index = 0

			plt.title(track.name)
			plt.title(track.id, loc='right')
			plt.show()