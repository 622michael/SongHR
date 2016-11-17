from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track
import matplotlib.pyplot as plt


## This command gets all average heart rates for all the listens

class Command(BaseCommand):
	def handle(self, *args, **options):
		tempos = []
		heartrates = []

		# for listen in Listen.objects.all():
		# 	if listen.average_heart_rate is None:
		# 		continue

		# 	duration = (listen.end - listen.start).total_seconds()
		# 	if duration < 60.0:
		# 		continue

		# 	if listen.track == None:
		# 		continue


		# 	try:
		# 		tempos.append(listen.track.tempo)
		# 		heartrates.append(listen.average_heart_rate)
		# 	except:
		# 		continue

		for track in Track.objects.all():
			listens = Listen.objects.filter(track = track)
			if len(listens) < 2:
				continue

			for listen in listens:
				if listen.average_heart_rate > 100:
					continue
					
				tempos.append(track.tempo)
				heartrates.append(listen.average_heart_rate)
			


		plt.plot(tempos, heartrates, 'ro')
		plt.show()


