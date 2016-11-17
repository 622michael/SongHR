from django.http import HttpResponse, HttpResponseRedirect
import json, requests
from django.utils import timezone
import urllib
from datetime import datetime, timedelta
from models import User, Listen
from fitbit_time import string_for_date

client_id = "227XGW"
scope_request_url = "https://www.fitbit.com/oauth2/authorize?"
access_token_request_url = "https://api.fitbit.com/oauth2/token"
base_64_clinet_id_secret_encode = "MjI3WEdXOmYyYTUyOTVkODFjYzNmOWZiMWRlN2Q2MzFkNWVkMWRl"
api_scope = ["activity", "heartrate", "location", "profile", "settings", "sleep", "weight"]
heartrate_api_call = "https://api.fitbit.com/1/user/-/activities/heart/date/%(date)s/1d/1sec/time/%(start)s/%(end)s.json"

##	Permissions Request
##  --------------------------------------
##	Loads the redirect to begin oauth process 
##
##

def permissions_request(request):
	base_url = scope_request_url
	scope = ""
	for data_point in api_scope: 
		scope += data_point + " "

	parameters = {"client_id": client_id, "scope": scope, "response_type": "code"}
	url = base_url + urllib.urlencode(parameters)

	redirect_reponse = HttpResponse("", status=302)
	redirect_reponse["location"] = url 
	return redirect_reponse

##	Authorize
##  --------------------------------------
##	handles the request from the fitbit server	
##  after a new user authorizes the app
##
def authorize(request):
	access_info, errors = request_access_info(code = request.GET['code'])
	if errors is not None:
		print errors
		return HttpResponse("", status = 502)

	user_id = access_info["user_id"]
	access_token = access_info["access_token"]
	scope = access_info["scope"]
	refresh_token = access_info["refresh_token"]
	expiration_date = timezone.now() + timedelta(seconds = access_info["expires_in"])

	try:
		user = User.objects.get(fitbit_id = user_id)
		user.fitbit_access_token = access_token
		user.fitbit_scope = scope
		user.fitbit_refresh_token = refresh_token
		user.fitbit_access_token_expiration = expiration_date
		user.save()

		return HttpResponse("", status = 204)
	except:
		user = User.objects.create( fitbit_id = user_id, 
								fitbit_access_token = access_token, 
								fitbit_access_token_expiration = expiration_date,
								fitbit_scope = scope, 
								fitbit_refresh_token = refresh_token)
		user.save()

	return HttpResponse("", status = 202)

##	Request Access Info
##  --------------------------------------
##	used get the user's authorization code 
##	param code is the code from fitbit server
##	returns access token, scope, refresh token

def request_access_info (code = "", refresh_token = "", grant_type = "authorization_code"):
	parameters = {'code': code, 'grant_type': grant_type, 'client_id': client_id, 'refresh_token': refresh_token}
	headers = {"content-type":"application/x-www-form-urlencoded", "Authorization": "Basic " + base_64_clinet_id_secret_encode}
	response = requests.post(access_token_request_url, headers= headers, data= parameters)
	json_response = json.loads(response.content)
	if json_response.get('success', True) is False:
		return None, json_response['errors']

	return json_response, None

##	Request Header
##  --------------------------------------
##	returns the header necessary to make
## 	an api calls. It also refreshes the
##	access token if it is out of date

def api_request_header_for(user):
	expiration_date = user.fitbit_access_token_expiration

	if expiration_date < timezone.now():
		refresh_access_for_user(user)

	headers = {'Authorization': 'Bearer ' + user.fitbit_access_token}
	return headers

##	Refresh Access
##  --------------------------------------
##	uses the refresh token to refresh the access token	
##
##
def refresh_access_for_user(user):
	access_info, errors = request_access_info(refresh_token = user.fitbit_refresh_token, grant_type = "refresh_token")
	if errors is not None:
		return None


	expiration_date = timezone.now() + timedelta(seconds = access_info["expires_in"])
	
	user.fitbit_access_token = access_info["access_token"]
	user.fitbit_refresh_token = access_info["refresh_token"]
	user.fitbit_access_token_expiration = string_for_date(expiration_date)
	user.save()

## Average Heart Rate During Listen
## --------------------------------------
## Gets the average heart rate during the time
## of the listen from the FitBit Intraday access
## info.

def average_heart_rate_during_listen(listen):
	date = listen.start.strftime("%Y-%m-%d")
	start = listen.start.strftime("%H:%M")
	end = listen.end.strftime("%H:%M")


	fitted_api_call = heartrate_api_call % {"date": date, "end": end, "start": start}
	headers = api_request_header_for(User.objects.first())
	response = requests.get(fitted_api_call, headers = headers)
	json_response = json.loads(response.content)

	print json_response



