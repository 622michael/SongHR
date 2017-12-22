from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import ListenAudioSegment
import math
class Command(BaseCommand):
	def handle(self, *args, **options):
		l_total = 0.0
		t_total = 0.0

		t_probs_total = 0.0
		l_probs_total = 0.0

		quantity = 0.0

		for l_a_segment in ListenAudioSegment.objects.all():
			print l_a_segment.id
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

			l_total += l_correlation
			t_total += t_correlation

			t_probs_total += 1.0 - t_probs_not_caused
			l_probs_total += 1.0 - l_probs_not_caused

			quantity += 1.0

		print "Average Tempo Correlation: %f" % (t_total/quantity)
		print "Average Loudness Correlation: %f" % (l_total/quantity)
		print "Average Tempo Probability: %f" % (t_probs_total/quantity)
		print "Average Loudness Probability: %f" % (l_probs_total/quantity)