from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate, AudioSegment
import matplotlib.pyplot as plt
from sfitbit import spotify, audio
import numpy as np


## This command gets all average heart rates for all the listens

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '-id',
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

		


		for track in Track.objects.all():
			if len(Listen.objects.filter(track = track)) < 3:
				print "Minimial listen"
				continue
			x = []
			y = []
			for listen in Listen.objects.filter(track = track):
				if listen.track is None:
					print "run 'python manage.py connect_track_to_listen' to insure all listens have a track."
					continue

				if len(HeartRate.objects.filter(listen = listen)) < 5:
					print "Skipping listen %i; minimal heart rate data" % (listen.id)
					continue

				audio_analysis, errors = spotify.audio_analysis_for(listen.track)
				tempos, times = spotify.loudness(listen.track, data = audio_analysis)

				for i in range(0, len(times)):
					tempo_time = times[i]
					if i == len(times) - 1:
						next_tempo_time = audio_analysis["track"]["duration"]
					else:
						next_tempo_time = times[i + 1]

					print "Looking for heartrates between %i - %i" % (tempo_time, next_tempo_time)
					for heartrate in HeartRate.objects.filter(listen = listen, time__gte = tempo_time, time__lte= next_tempo_time):
						y.append(float(heartrate.z_score))
						x.append(tempos[i])

			plt.plot(x, y, 'ro')
			plt.title(track.name)
			plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
			plt.show()
