from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate, ListenAudioSegment, AudioSegment
import matplotlib.pyplot as plt
from sfitbit import spotify, audio, heart_rates
import numpy as np
import math
import random


## This command gets all average heart rates for all the listens

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '--id',
            action='store',
            dest='listen_id',
            default=None,
            help='Display graph for a specific song') 

		parser.add_argument('--random',action='store',
            dest='random',
            default= False,
            help='Choose the next graph randomly'
        )

	def handle(self, *args, **options):

		if options["listen_id"] is not None:
			l_a_segments = ListenAudioSegment.objects.filter(listen_id = options["listen_id"])
		else:
			l_a_segments = ListenAudioSegment.objects.all()
			if options["random"]:
				l_a_segments = l_a_segments[:len(l_a_segments)]
				l_a_segments = sorted(l_a_segments, key=lambda x: random.random())
			

		print 'id \t \t Loudness \t \t Tempo'
		print '--------------------------------------------'
		for l_a_segment in l_a_segments:
			l_probs_not_caused = 0
			t_probs_not_caused = 0
			
			l_correlation = abs(float(l_a_segment.hr_loudness_correlation))
			t_correlation = abs(float(l_a_segment.hr_tempo_correlation))

			if l_correlation < 1:
				l_probs_not_caused = math.exp(-2 * math.pi * l_correlation)
			else:
				l_probs_not_caused = math.exp(-2 * math.pi * (1/l_correlation))

			if t_correlation < 1:
				t_probs_not_caused = math.exp(-2 * math.pi * t_correlation)
			else:
				t_probs_not_caused = math.exp(-2 * math.pi * (1/t_correlation))

			print '%(id)i \t \t %(l)f \t \t %(t)f' % {"id": l_a_segment.id, "l": l_probs_not_caused, "t": t_probs_not_caused}

			if  1 - l_probs_not_caused > .90 or 1 - t_probs_not_caused > .90:
				average_heartrate = average_heartrate = heart_rates.average_heart_rate(l_a_segment.listen)

				tempo_offset = average_heartrate - float(l_a_segment.listen.track.tempo)
				loudness_offset = average_heartrate - float(l_a_segment.listen.track.loudness)
				tempos, loudnesses, times = audio.tempo_loudness_time_arrays(l_a_segment.listen.track, 
					tempo_offset = tempo_offset, loudness_offset = loudness_offset)
				plt.plot(times, tempos, "b")
				plt.plot(times, loudnesses, "g")

				heartrates, times = heart_rates.heart_rate_time_arrays(l_a_segment.listen)
				plt.plot(times, heartrates, "r")

				plt.plot([l_a_segment.audio_segment.time], [float(l_a_segment.audio_segment.tempo) + tempo_offset], "bo")
				plt.plot([l_a_segment.audio_segment.time], [float(l_a_segment.audio_segment.loudness) + loudness_offset], "go")

				heart_rate = heart_rates.heart_rate_at_time(l_a_segment.listen, l_a_segment.audio_segment.time)
				if 1 - l_probs_not_caused > .90:
					plt.plot([heart_rate.time], [heart_rate.value], "go")
				if 1 - t_probs_not_caused > .90:
					plt.plot([heart_rate.time], [heart_rate.value], "bo")

				plt.show()

