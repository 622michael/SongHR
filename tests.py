import requests
import time


result = requests.post("http://127.0.0.1:8000/log/track/", data = {"album": "Blonde", "artist": "Frank Ocean", "track": "Nights"})
print result

time.sleep(4)

result = requests.post("http://127.0.0.1:8000/log/end/", data = {"album": "Blonde", "artist": "Frank Ocean", "track": "Nights"})
print result