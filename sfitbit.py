## This script takes in three variables as input: title, album, artist
## Returns the Spotiy ID of the track
## E.g. "python sfitbit.py TRACK ALBUM ARTIST"

import spotipy
import sys 


title = sys.argv[1]
album = sys.argv[2]
artist = sys.argv[3]

sp = spotipy.Spotify()
results = sp.search(q = "track:%s album:%s artist:%s" % (title, album, artist), limit = 1)
print results["tracks"]["items"][0]["ids"]
