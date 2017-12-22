from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate, AudioSegment
from sfitbit import spotify
from datetime import datetime, timedelta, time
import pytz

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '--id',
            action='store',
            dest='track_id',
            default=None,
            help='Select a track to download audio segments for',
        )

	def handle(self, *args, **options):
		if options["track_id"] is not None:
			try:
				tracks = Track.objects.get(id = options["track_id"])
			except:
				print "Invalid ID"
				return
		else:
			tracks = Track.objects.all()

		for track in tracks:
			if len(AudioSegment.objects.filter(track = track)) > 1:
				continue

			audio_analysis, errors = spotify.audio_analysis_for(track)
		
			if errors is not None:
				continue

			for segment in audio_analysis["sections"]:
				a = AudioSegment.objects.create(time = segment["start"],
											tempo = segment["tempo"],
											loudness = segment["loudness"],
											duration = segment["duration"],
											track = track)
				a.save()