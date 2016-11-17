from django.db import models

class User(models.Model):
	fitbit_id = models.CharField(max_length = 25)
	fitbit_access_token = models.CharField(max_length = 260)
	fitbit_scope = models.CharField(max_length = 260)
	fitbit_refresh_token= models.CharField(max_length = 64)
	fitbit_access_token_expiration = models.DateTimeField()

	spotify_access_token = models.CharField(max_length = 260, null = True)
	spotify_scope = models.CharField(max_length = 260, null = True)
	spotify_refresh_token= models.CharField(max_length = 131, null = True)
	spotify_access_token_expiration = models.DateTimeField(null = True)

class Album(models.Model):
	spotify_id = models.CharField(max_length = 22)
	name = models.CharField(max_length = 22)

class Artist(models.Model):
	spotify_id = models.CharField(max_length = 22)
	name = models.CharField(max_length = 260)
	albums = models.ManyToManyField(Album)

class Track(models.Model):
	spotify_id = models.CharField(max_length = 22)
	name = models.CharField(max_length = 260)
	album = models.ForeignKey(Album, on_delete = models.CASCADE)
	artists = models.ManyToManyField(Artist)

	tempo = models.DecimalField(max_digits = 10, decimal_places = 3, null = True)

## Represents an instances of a song being
## listened to.
class Listen(models.Model):
	song_spotify_id = models.CharField(max_length = 22)
	start = models.DateTimeField(auto_now_add = True)
	end = models.DateTimeField(null = True)
	ended = models.IntegerField(default = 0)
	track = models.ForeignKey(Track, on_delete = models.CASCADE, null = True)
	average_heart_rate = models.DecimalField(max_digits = 6, decimal_places = 2, null = True)