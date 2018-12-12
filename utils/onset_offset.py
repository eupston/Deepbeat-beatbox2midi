import librosa
import numpy as np

def onset_offset(sr, onset, onsetframes, silences):

	##----------Converts Silences Milliseconds to frames-------
	silences_frames = []
	for items in silences:
		silences_frames.append([round(items[0]*(sr/1000)), round(items[1]*(sr/1000))])
	#-------------------------------------------------------------------

	##--------------------------------------------

	onset_frames = onsetframes.tolist()

	#grabs the onset and offset based on silences threshold and onset detected
	onset_offset =[]
	for i, onset in enumerate(onset_frames):
		if onset != onset_frames[-1]:
			issilence = [silence[0] for silence in silences_frames if silence[0] > onset and silence[0] < onset_frames[i+1]]
			if len(issilence) > 0:
				onset_offset.append([onset, issilence[0]])
			else:
				onset_offset.append([onset,onset_frames[i+1]])
		else:
			onset_offset.append([onset,silences_frames[-1][0]])

	#return onset and offsets in frames
	return onset_offset
