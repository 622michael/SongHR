from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, ListenAudioSegment, AudioSegment, HeartRate
import matplotlib.pyplot as plt
import numpy as np
from sfitbit import fitbit, audio, heart_rates
from datetime import datetime, timedelta, time
import pytz
from sfitbit import spotify
from decimal import * 

class Command(BaseCommand):
	def handle(self, *args, **options):
		for listen in Listen.objects.all():
			if HeartRate.objects.filter(listen = listen).first() is None:
				print "no heart rate"
				continue
			if HeartRate.objects.filter(listen = listen).first().z_score is not None:
				print "already have z_score"
				continue

			hrs = np.array([])
			for sec in range (0, int((listen.end - listen.start).total_seconds())):
				hr = heart_rates.heart_rate_at_time(listen, sec)
				if hr is None:
					continue
					
				hr = float(hr.value)
				hrs = np.append(hrs, hr)

			listen_average_hr = np.mean(hrs)
			listen_hr_std = np.std(hrs)

			for hr in HeartRate.objects.filter(listen = listen):
				print hr.id
				
				z_score = ((float(hr.value) - listen_average_hr)/listen_hr_std)
				try:
					hr.z_score = z_score
					hr.save()
				except InvalidOperation:
					print z_score
					print "Cannot quanitze"
					continue
