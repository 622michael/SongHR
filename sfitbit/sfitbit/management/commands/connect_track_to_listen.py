from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track


## This command gets all average heart rates for all the listens

class Command(BaseCommand):
	def handle(self, *args, **options):
		for listen in Listen.objects.all():
			try:
				track = Track.objects.get(spotify_id = listen.song_spotify_id)
				listen.track = track
				listen.save()
			except:
				next