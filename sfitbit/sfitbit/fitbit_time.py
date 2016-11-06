import pytz
from datetime import datetime
import dateutil

def remove_timezone_from_string(string):
	return string[:-6]

def convert_isoweekday_to_string(isoweekday):
	if isoweekday is 1:
		return "MONDAY"
	elif isoweekday is 2:
		return "TUESDAY"
	elif isoweekday is 3:
		return "WEDNESDAY"
	elif isoweekday is 4:
		return "THURSDAY"
	elif isoweekday is 5:
		return "FRIDAY"
	elif isoweekday is 6:
		return "SATURDAY"
	elif isoweekday is 7:
		return "SUNDAY"

def time_from_date(date):
	if date.utcoffset() is not None:
		utc_offset = int(date.utcoffset().total_seconds()/3600)
	else:
		utc_offset = 0.0

	utc_offset_string = ""
	if utc_offset < 0:
		utc_offset_string = "-%02d:00" % abs(utc_offset)
	else:
		utc_offset_string = "+%02d:00" % abs(utc_offset)

	fitbit_time = "%02d:%02d" % (date.hour, date.minute) + utc_offset_string

	return fitbit_time

def string_for_date(date, time = True):
	date_string = "%(year)02d-%(month)02d-%(day)02d" % {'year': date.year, 'month': date.month, 'day': date.day}

	if not time:
		return date_string
	else:
		time_string = time_from_date(date)
		return date_string + " " + time_string

def date_for_string(string):
	return datetime.strptime(remove_timezone_from_string(string), "%Y-%m-%d %H:%M")

def log_date_for_string(user, string):
	return pytz.timezone(user.timezone).localize(datetime.strptime(string[:-4], "%Y-%m-%dT%H:%M:%S"))

def now():
	return datetime.now().replace(tzinfo=dateutil.tz.tzoffset(None, 0))


def timezone_offset(string):
	return int(string[16:19])
