from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, AudioSegment, ListenAudioSegment
from sfitbit import heart_rates
from sfitbit import audio

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
			if len(heart_rates.heart_rates_in_listen(listen)) < 3:
				continue

			for audio_segment in audio.audio_segments_in_track(listen.track):
				try:
					audio_segment = ListenAudioSegment.objects.get(listen = listen, audio_segment = audio_segment)
				except:
					a = ListenAudioSegment.objects.create(listen = listen,
													audio_segment = audio_segment)

					try:
						average_hr = heart_rates.average_heart_rate(listen, start_time = audio_segment.time, 
																end_time = audio_segment.time + audio_segment.duration)
						a.average_heart_rate = average_hr
					except:
						continue 

					try:
						hr_slope = heart_rates.slope_between_times(listen, audio_segment.time, audio_segment.time + audio_segment.duration)
						l_slope = audio.loudness_slope(listen.track, audio_segment.time, audio_segment.time + audio_segment.duration)
						t_slope = audio.tempo_slope(listen.track, audio_segment.time, audio_segment.time + audio_segment.duration)
					except EnvironmentError:
						continue
					except ZeroDivisionError:
						continue

					if l_slope != 0.0:
						hr_l_correlation = hr_slope/l_slope
						a.hr_loudness_correlation = hr_l_correlation

					if t_slope != 0.0:
						hr_t_correlation = hr_slope/t_slope
						a.hr_tempo_correlation = hr_t_correlation

					a.save()