from django.core.management.base import BaseCommand, CommandError
from sfitbit.models import Listen
from sfitbit import fitbit


## This command gets all average heart rates for all the listens

class Command(BaseCommand):
	def handle(self, *args, **options):
		for listen in Listen.objects.all():
			fitbit.average_heart_rate_during_listen(listen)