from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track
import matplotlib.pyplot as plt
import numpy as np
from sfitbit import fitbit

class Command(BaseCommand):
	def handle(self, *args, **options):
		tempos = []
		delta_heartrates = []

		for track in Track.objects.all():
			listens = Listen.objects.filter(track = track)
			if len(listens) < 2:
				continue

			for listen in listens:
				# if listen.average_heart_rate is None:
				# 	continue

				try:
					heartrate_data = fitbit.heart_rate_data_for_listen(listen)["activities-heart-intraday"]["dataset"]

					intial_heart_rate = int(heartrate_data[0]["value"])
					final_heart_rate = int(heartrate_data[len(heartrate_data) - 1]["value"])
					delta_heart_rate = final_heart_rate - intial_heart_rate

					print "%i became %i in %s" % (intial_heart_rate, final_heart_rate, listen.track.name)

					delta_heartrates.append(delta_heart_rate)
					tempos.append(track.tempo)
				except:
					continue

		plt.plot(tempos, delta_heartrates, 'ro')
		# fit with np.polyfit
		m, b = np.polyfit(tempos, delta_heartrates, 1)
		print "Fit: %f * x + %f" % (m, b)

		plt.show()