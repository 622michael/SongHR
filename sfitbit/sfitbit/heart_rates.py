from sfitbit.models import Listen, Track, HeartRate
import pytz
from datetime import datetime, timedelta

## A controller that is responsible for interpretting all
## data that has to do with heart rates, dealing with the
## heart rate during Listens.

## Heart Rate, Time Arrays
## ------------------------------------
## Returns the heart rates and times of
## the heart rates for a given listen in
## two seperate arrays.

def heart_rate_time_arrays(listen):
	heart_rates = []
	times = []

	for heart_rate in heart_rates_in_listen(listen):
		heart_rates.append(heart_rate.value)
		times.append(heart_rate.time)

	return heart_rates, times

## Average Heart Rate
## ------------------------------------
## Returns the average heart rate during
## a listen.
##

def average_heart_rate(listen, start_time = None, end_time = None):
	heart_rates = heart_rates_in_listen(listen)

	if len(heart_rates) < 2:
		return 0

	running_sum = 0.0
	duration = 0.0
	for i in range(1, len(heart_rates)):
		t_start_time = heart_rates[i - 1].time
		if (start_time is not None and end_time is not None and
			t_start_time > end_time):
			continue

		t_end_time = heart_rates[i].time

		hr_duration = t_end_time - t_start_time
		duration += hr_duration
		running_sum += heart_rates[i - 1].value * hr_duration

	return running_sum/duration



## Time In Listen
## ------------------------------------
## Returns the second that the heart_rate
## occurs in the listen. Heart rate can 
## either be a dictionary (with ["time"])
## or from the heart rate model.

def time_in_listen(heart_rate, listen):
	local = pytz.timezone("US/Eastern")
	listen_start = listen.start.astimezone(local)

	if type(heart_rate) is dict:
		absolute_time = datetime.strptime(heart_rate["time"], "%H:%M:%S").replace(tzinfo = local)
		absolute_time = absolute_time.replace(day = listen_start.day, year = listen_start.year, month = listen_start.month)
	else:
		absolute_time = datetime.strptime(heart_rate.time, "%H:%M:%S").replace(tzinfo = local)
		absolute_time = absolute_time.replace(day = listen_start.day, year = listen_start.year, month = listen_start.month)

	return (absolute_time - listen_start).total_seconds()

## Slope Between Times
## ------------------------------------
## Returns the slope in the heart rate
## Between two times.

def slope_between_times(listen, start_time, end_time):
	start_heart_rate = heart_rate_at_time(listen, start_time)
	end_heart_rate = heart_rate_at_time(listen, end_time)
	delta_heart_rate = change_in_heart_rate(listen, start_time, end_time)
	duration = float(end_heart_rate.time - start_heart_rate.time)

	if duration == 0.0:
		raise EnvironmentError

	
	return delta_heart_rate/duration

## Change in Heart Rate
## ------------------------------------
## Returns the change in heart rate that occurs
## between the start time and the end time.

def change_in_heart_rate(listen, start_time, end_time):
	start_heart_rate = heart_rate_at_time(listen, start_time)
	end_heart_rate = heart_rate_at_time(listen, end_time)

	if start_heart_rate is None or  end_heart_rate is None:
		raise EnvironmentError

	if start_heart_rate.id == end_heart_rate.id:
		try:
			end_heart_rate = HeartRate.objects.get(listen = listen, 
				id = start_heart_rate.id + 1)
		except:
			## TODO: throw exception
			return 0

	return end_heart_rate.value - start_heart_rate.value

## Heart Rates In Listen
## ---------------------------------------
## Gives all the heart rates for a listen
##
##

def heart_rates_in_listen(listen):
	return HeartRate.objects.filter(listen = listen)


## Heart Rate At Time
## ---------------------------------------
## Returns the a heart rate object that is from
## the last sample taken. Closests to that time.

def heart_rate_at_time(listen, time):
	return HeartRate.objects.filter(listen = listen, time__lte = time).last()