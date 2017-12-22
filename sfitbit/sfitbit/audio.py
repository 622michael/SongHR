from models import AudioSegment

## This controller is responsibile for handling
## all interpretation of audio data. Mostly focused
## on the tempo and beats. Manages AudioSegement model.

## Tempo, Loudness, Time Arrays
## ------------------------------------
## Splits the variables from the audio
## segments in a given track into three
## seperate arrays. 
## Extremely useful for graphing.

def tempo_loudness_time_arrays(track, tempo_offset = 0, loudness_offset = 0):
	tempos = []
	loudnesses = []
	times = []

	for audio_seg in AudioSegment.objects.filter(track = track):
		tempos.append(float(audio_seg.tempo) + tempo_offset)
		loudnesses.append(float(audio_seg.loudness) + loudness_offset)
		times.append(audio_seg.time)

	return tempos, loudnesses, times


## Tempo Slope
## ------------------------------------
## The slope of the tempo vs. time graph
## for a given track between two points.
##

def tempo_slope(track, start_time, end_time):
	if start_time is end_time:
		raise ValueError

	start_audio_segment = audio_segment_at_time(track, start_time)
	end_audio_segment = audio_segment_at_time(track, end_time)

	if start_audio_segment.id is end_audio_segment.id:
		return 0

	delta_tempo = change_in_tempo(track, start_time, end_time)
	delta_t = end_audio_segment.time - start_audio_segment.time

	if float(delta_t) == 0:
		raise ZeroDivisionError

	return float(delta_tempo)/float(delta_t)

## Loudness Slope
## ------------------------------------
## The slope of the loudness vs. time graph
## for a given track between two points.
##

def loudness_slope(track, start_time, end_time): 
	if start_time is end_time: 
		raise ValueError

	start_audio_segment = audio_segment_at_time(track, start_time)
	end_audio_segment = audio_segment_at_time(track, end_time)

	if start_audio_segment.id is end_audio_segment.id:
		return 0

	delta_l = change_in_loudness(track, start_time, end_time)
	delta_t = end_audio_segment.time - start_audio_segment.time

	if float(delta_t) == 0:
		return ZeroDivisionError

	return float(delta_l)/float(delta_t)

## Change In Tempo
## ------------------------------------
## The change in tempo between two points
##
##

def change_in_tempo(track, start_time, end_time):
	start_tempo = tempo_at_time(track, start_time)
	end_tempo = tempo_at_time(track, end_time)
	return end_tempo - start_tempo

## Change In Loudness
## ------------------------------------
## The change in loudness between two points
##
##

def change_in_loudness(track, start_time, end_time):
	start_loudness = loudness_at_time(track, start_time)
	end_loudness = loudness_at_time(track, end_time)
	return end_loudness - start_loudness

## Tempo At Time
## ------------------------------------
## Gets the tempo in a given track at the
## time in the track.
##

def tempo_at_time(track, time):
	audio_segment = audio_segment_at_time(track, time)
	return audio_segment.tempo
	
## Loudness At Time
## ------------------------------------
## Gets the tempo in a given track at the
## time in the track.
##

def loudness_at_time(track, time):
	audio_segment = audio_segment_at_time(track, time)
	return audio_segment.loudness

## Audio Segment In Track
## ------------------------------------
## Returns the Audio Segments in a given
## track.
##

def audio_segments_in_track(track):
	return AudioSegment.objects.filter(track = track)

## Audio Segment At time
## ------------------------------------
## Returns the details about the audio at 
## a given time in the track.
##

def audio_segment_at_time(track, time):
	if time < 0:
		raise ValueError
	if time > track.duration:
		raise ValueError

	return AudioSegment.objects.filter(track = track, time__lte = time).last()