from django.db import models

## Represents an instances of a song being
## listened to.
class Listen(models.Model):
	song_spotify_id = models.CharField(max_length = 22)
	listened_at = models.DateTimeField(auto_now_add = True)


class User(models.Model):
	fitbit_id = models.CharField(max_length = 25)
	access_token = models.CharField(max_length = 260)
	scope= models.CharField(max_length = 260)
	refresh_token= models.CharField(max_length = 64)
	access_token_expiration = models.DateTimeField()