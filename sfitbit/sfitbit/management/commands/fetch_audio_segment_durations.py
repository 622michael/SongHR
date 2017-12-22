from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate, AudioSegment
from sfitbit import spotify
from sfitbit import audio
from datetime import datetime, timedelta, time
import pytz

class Command(BaseCommand):
	def handle(self, *args, **options):
		for track in Track.objects.all():
			audio_segments = audio.audio_segments_in_track(track)
			for i in range(1, len(audio_segments)):
				audio_segment = audio_segments[i - 1]
				next_audio_segment = audio_segments[i]
				if i is len(audio_segments) - 1:
					duration = track.duration - next_audio_segment.time
					next_audio_segment.duration = duration
					next_audio_segment.save()

				duration = next_audio_segment.time - audio_segment.time
				audio_segment.duration = duration
				audio_segment.save()