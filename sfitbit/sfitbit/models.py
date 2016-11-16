from django.db import models

## Represents an instances of a song being
## listened to.
class Listen(models.Model):
	song_spotify_id = models.CharField(max_length = 22)
	start = models.DateTimeField(auto_now_add = True)
	end = models.DateTimeField(auto_now = True, null = True)
	ended = models.IntegerField(default = 0)


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
