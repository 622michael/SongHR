from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate
import matplotlib.pyplot as plt
from sfitbit import spotify, audio
from sfitbit import heart_rates as hr
import numpy as np


## This command gets all average heart rates for all the listens

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '--id',
            action='store',
            dest='listen_id',
            default=None,
            help='Display graph for a specific song',
        )

	def handle(self, *args, **options):
		if options["listen_id"] is not None:
			try:
				listens = [Listen.objects.get(id = options["listen_id"])]
			except:
				print "invaid id"
				return 
		else:
			listens = Listen.objects.all()

		for listen in listens:
			if listen.track is None:
				print "run 'python manage.py connect_track_to_listen' to insure all listens have a track."
				continue

			if len(HeartRate.objects.filter(listen = listen)) < 5:
				print "Skipping listen %i; minimal heart rate data" % (listen.id)
				continue

			track = listen.track

			heart_rates = hr.heart_rates_in_listen(listen)
			audio_segs = audio.audio_segments_in_track(track)
			num_heart_rates = len(heart_rates)
			num_audio_seg = len(audio_segs)

			
			times = []
			
			if num_heart_rates < num_audio_seg:
				for i in range(1, num_heart_rates):
					start_time = heart_rates[i - 1].time
					end_time = heart_rates[i].time
					times.append((start_time, end_time))
			else:
				for i in range(1, num_audio_seg):
					start_time = audio_segs[i - 1].time
					end_time = audio_segs[i].time
					times.append((start_time, end_time))

			loudness_correlations = []
			tempo_correlations = []
			x_lc = []
			x_tc = []
			for start_time, end_time in times:
				if start_time == end_time:
					continue

				try:	
					hr_slope = hr.slope_between_times(listen, start_time, end_time)
				except EnvironmentError:
					continue
				
				try:
					l_slope = audio.loudness_slope(listen.track, start_time, end_time)
					t_slope = audio.tempo_slope(listen.track, start_time, end_time)
				except ValueError:
					continue
				except ZeroDivisionError:
					continue

				if l_slope != 0.0:
					loudness_correlation = hr_slope/l_slope
					loudness_correlations.append(loudness_correlation)
					x_lc.append(float(start_time + end_time)/2.0)
				if t_slope != 0.0:
					tempo_correlation = hr_slope/t_slope
					tempo_correlations.append(tempo_correlation)
					x_tc.append(float(start_time + end_time)/2.0)


			plt.plot(x_lc, loudness_correlations, "ro")
			plt.plot(x_tc, tempo_correlations, "bo")
			plt.title(listen.track.name)
			plt.title(listen.track.id, loc='right')
			plt.title(listen.id, loc='left')
			plt.show()
