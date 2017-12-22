from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen, Track, HeartRate
from sfitbit import fitbit, heart_rates
from datetime import datetime, timedelta, time
import pytz

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
            '-id',
            action='store',
            dest='listen_id',
            default=None,
            help='Select a listen to download heart rate data for',
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
			if len(HeartRate.objects.filter(listen = listen)) > 1:
				continue
				
			local = pytz.timezone("US/Eastern")
			listen_start = listen.start.astimezone(local)

			heartrates = fitbit.heart_rate_data_for_listen(listen)["activities-heart-intraday"]["dataset"]

			for heartrate in heartrates: 
				time_since_start = heart_rates.time_in_listen(heartrate, listen)
				
				try:
					hr.get(listen = listen, time = time_since_start, value = heartrate["value"])
				except:
					hr = HeartRate.objects.create(listen = listen, time = time_since_start, value = heartrate["value"])
					hr.save()