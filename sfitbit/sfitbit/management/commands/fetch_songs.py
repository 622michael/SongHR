from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, Album, Artist
from sfitbit import spotify


## This command gets all listens and insures that songs have
## been created from them. Needed to update to newer version
## where songs are stored in the database as more than just a
## spotify id.

class Command(BaseCommand):
	def handle(self, *args, **options):
		for listen in Listen.objects.all():
			spotify.save_track_from_spotify_id(listen.song_spotify_id)
