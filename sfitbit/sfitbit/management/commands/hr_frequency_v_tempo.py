from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate, AudioSegment
import matplotlib.pyplot as plt
from sfitbit import spotify, audio, heart_rates
import numpy as np


class Command(BaseCommand):
	def handle(self, *args, **options):
		x = []
		y = []

		for track in Track.objects.all():
			listens = Listen.objects.filter(track = track)
			if len(listens) < 2:
				continue

			running_period_sum = 0.0
			count = 0.0
			for listen in listens:
				if len(HeartRate.objects.filter(listen = listen)) < 5:
					print "Skipping listen %i; minimal heart rate data" % (listen.id)
					continue

				hrs, times = heart_rates.heart_rate_time_arrays(listen)

				running_duration_sum = 0
				for i in range(1, len(times)):
					duration = times[i] - times[i - 1]
					print duration 
					running_duration_sum += duration
				
				average_duration = float(running_duration_sum)/float(len(times))
				print average_duration
				running_period_sum += average_duration
				count += 1

			if count < 1:
				continue

			average_period = float(running_period_sum)/float(count)
			y.append(average_period)
			x.append(float(track.tempo))


		plt.plot(x, y, 'ro')
		plt.title(track.name)
		plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
		plt.show()
