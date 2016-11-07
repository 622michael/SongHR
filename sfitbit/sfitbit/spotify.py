import spotipy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from models import Listen

## Responsible for handling all spotify entries
## into the database.
## ---------------------------------------------


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

	data_sample = Listen.objects.create(song_spotify_id = track_id)
	data_sample.save()

	response = HttpResponse("", status = 202)
	return response

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


def song_id(track, album, artist):
	sp = spotipy.Spotify()
	query = "track:%s album:%s artist:%s" % (track, album, artist)
	results = sp.search(q = query, limit = 1)
	track_id = results["tracks"]["items"][0]["id"]

	return track_id