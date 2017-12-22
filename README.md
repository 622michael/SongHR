This project is no longer being developed

# Description

This source code was used to compare the heart rate monitor of FitBit against the loudness and tempo of songs (as determined by the Spotify API). It has a django server that allows users to authenticate their Spotify and FitBit accounts.

When this was developed, the Spotify API did not release user's recently played songs. The SpotifyReporter.scpt reports the currently playing song and when it stops playing to the server.

There are Django management commands that allow the admin to view graphs that show the correlation between the heartrate and tempo of songs.

This provides the basis for a study that could be conducted to determine if there is any correlation between the loudness or tempo of a song.


