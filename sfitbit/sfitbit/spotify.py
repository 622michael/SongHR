import spotipy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from models import Listen, User, Track, Artist, Album
import json, requests
from datetime import datetime, timedelta

## Responsible for handling all spotify entries
## into the database.
## ---------------------------------------------

client_id = "404f9c1778dd4730812ab807ca52aeff"
access_token_request_url = "https://accounts.spotify.com/api/token"
base_64_clinet_id_secret_encode = "NDA0ZjljMTc3OGRkNDczMDgxMmFiODA3Y2E1MmFlZmY6MmUyNjE5ZWE1MzZlNDEyM2E2ZmNkYTdlMGIyM2FjYzQ="
spotify_redirect = "http://127.0.0.1:8000/user/spotify/register"


##	Authorize
##  --------------------------------------
##	handles the request from the spotify server	
##  after a new user authorizes the app
##
def authorize(request):
	access_info, errors = request_access_info(code = request.GET['code'])
	if errors is not None:
		print errors
		return HttpResponse("", status = 502)

	access_token = access_info["access_token"]
	refresh_token = access_info["refresh_token"]
	expiration_date = timezone.now() + timedelta(seconds = access_info["expires_in"])

	try:
		user = User.objects.first()
		user.spotify_access_token = access_token
		user.spotify_refresh_token = refresh_token
		user.spotify_access_token_expiration = expiration_date
		user.save()

		return HttpResponse("", status = 204)
	except:
		user = User.objects.create( spotify_access_token = access_token, 
								spotify_access_token_expiration = expiration_date,
								spotify_scope = scope, 
								spotify_refresh_token = refresh_token)
		user.save()

	return HttpResponse("", status = 202)

##	Request Access Info
##  --------------------------------------
##	used get the user's authorization code 
##	param code is the code from spotify server
##	returns access token, scope, refresh token

def request_access_info (code = "", refresh_token = "", grant_type = "authorization_code"):
	parameters = {'code': code, 'grant_type': grant_type, 'client_id': client_id, 'refresh_token': refresh_token, 'redirect_uri': spotify_redirect}
	headers = {"content-type":"application/x-www-form-urlencoded", "Authorization": "Basic " + base_64_clinet_id_secret_encode}
	response = requests.post(access_token_request_url, headers= headers, data= parameters)
	json_response = json.loads(response.content)
	print json_response
	if json_response.get('success', True) is False:
		return None, json_response['errors']

	return json_response, None

##	Request Header
##  --------------------------------------
##	returns the header necessary to make
## 	an api calls. It also refreshes the
##	access token if it is out of date

def api_request_header_for(user):
	expiration_date = user.spoitfy_access_token_expiration

	if expiration_date < datetime.now() and not settings.TESTING:
		refresh_access_for_user(user)

	headers = {'Authorization': 'Bearer ' + user.spotify_access_token}
	return headers

##	Refresh Access
##  --------------------------------------
##	uses the refresh token to refresh the access token	
##
##
def refresh_access_for_user(user):
	access_info, errors = request_access_info(refresh_token = user.refresh_token, grant_type = "refresh_token")
	if errors is not None:
		return None


	expiration_date = timezone.now() + timedelta(seconds = access_info["expires_in"])
	
	user.spotify_access_token = access_info["access_token"]
	user.spotify_refresh_token = access_info["refresh_token"]
	user.spotify_access_token_expiration = fitbit_time.string_for_date(expiration_date)
	user.save()

##	Log
##  --------------------------------------
## Takes a title, album, and artist and records
## that it has been listened to. Uses the Spotify
## API to search for the song and selects only
## the first result based on those three criteria.
## Simply adds an entry into the database.
## @precondition request is POST.
## @precondition request has parameters: Artist, Album, Track

@csrf_exempt
def log(request):
	if request.method == "GET":
		not_found_response = HttpResponse("", status = 404)
		return not_found_response

	artist = request.POST["artist"]
	album  = request.POST["album"]
	track  = request.POST["track"]
	try:
		track_id = song_id(track, album, artist)
	except:
		return HttpResponse("", status = 404)

	data_sample = Listen.objects.create(song_spotify_id = track_id,
										track = save_track_from_spotify_id(track_id))
	data_sample.save()

	response = HttpResponse("", status = 202)
	return response

##	End Log
##  --------------------------------------
## Takes a title, album, and artist and records
## that it has been listened to. Uses the Spotify
## API to search for the song and selects only
## the first result based on those three criteria. 
## Sets the current date for the end date on the
## last listen entry with the same spotify id.
## @precondition request is POST.
## @precondition request has parameters: Artist, Album, Track
@csrf_exempt
def end_log(request):
	if request.method == "GET":
		return HttpResponse("", status = 404)

	artist = request.POST["artist"]
	album  = request.POST["album"]
	track  = request.POST["track"]
	try:
		track_id = song_id(track, album, artist)
	except:
		return HttpResponse("", status = 404)

	started_listen = Listen.objects.filter(song_spotify_id = track_id).latest('start')
	print started_listen.id
	if started_listen is None:
		return HttpResponse("", status = 404)
	if started_listen.ended is 1:
		return HttpResponse("", status = 409)

	started_listen.ended  = 1
	started_listen.save()

	return HttpResponse("", status = 202)

##	Song Id
##  --------------------------------------
##  Uses spotipy to query the spotify API
##  with the artist, album, and track. Returns
##  the ID of the first result.

def song_id(track, album, artist):
	sp = spotipy.Spotify()
	query = "track:%s album:%s artist:%s" % (track, album, artist)
	results = sp.search(q = query, limit = 1)
	track_id = results["tracks"]["items"][0]["id"]

	return track_id

##	Song Id
##  --------------------------------------
##  Uses spotipy to query the spotify API
##  for the information about the song given by the
##  track's spotify id. An object is created if and
##  only if the id doesn't already exist in the database
##  either returns the id of the new object or the 
##  object in the database.

def save_track_from_spotify_id(track_id):
	try:
		track = Track.objects.get(spotify_id = track_id)
	except:
		sp = spotipy.Spotify()
		track_json = sp.track(track_id)
		album_json = track_json["album"]

		try:
			album = Album.objects.get(spotify_id = album_json["id"])
		except:
			album = Album.objects.create(spotify_id = album_json["id"],
										 name = album_json["name"])
			album.save()

		track = Track.objects.create(spotify_id = track_id,
									 name = track_json["name"],
									 album = album)
		track.save()

		for artist_json in track_json["artists"]:
			try:
				artist = Artist.objects.get(spotify_id = artist_json["id"])
			except: 
				artist = Artist.objects.create(spotify_id = artist_json["id"],
												name = artist_json)
				artist.albums.add(album)
				artist.save()

				track.artists.add(artist)
		track.save()
		print "Added %s..." % track.name

	return track


		
