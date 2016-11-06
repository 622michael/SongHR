import spotipy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Listen

## Responsible for handling all spotify entries
## into the database
##


## Takes a title, album, and artist and records
## that it has been listened to. Uses the Spotify
## API to search for the song and selects only
## the first result based on those three criteria.
## Simply adds an entry into the database.
## @precondition request is POST.
## @precondition request has parameters: Artist, Album, Track

@csrf_exempt
def log(request):
	print request
	if request.method == "GET":
		not_found_response = HttpResponse("", status = 404)
		return not_found_response

	artist = request.POST["artist"]
	album  = request.POST["album"]
	track  = request.POST["track"]

	sp = spotipy.Spotify()
	query = "track:%s album:%s artist:%s" % (track, album, artist)
	results = sp.search(q = query, limit = 1)
	track_id = results["tracks"]["items"][0]["id"]
	print track_id

	data_sample = Listen.objects.create(spotify_id = track_id)
	data_sample.save

	response = HttpResponse("", status = 202)
	return response