from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Track
from sfitbit import spotify


## This command gets all the tempos for all the tracks in the database

class Command(BaseCommand):
	def handle(self, *args, **options):
		for track in Track.objects.all():
			spotify.save_track_tempo(track)