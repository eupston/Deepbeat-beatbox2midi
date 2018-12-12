from mido import Message, MidiFile, MidiTrack
import mido
import librosa
import numpy as np
from keras import backend as K
import tensorflow as tf
import os
#my classes
from .predict import predict_one, load_model_ext
from .remove_silence import remove_silence
from .onset_offset import onset_offset


def audio2midi(wavfile, modelpath):

	#---------- Removes Silence under Threshold----------#
	silences = remove_silence(wavfile, thresh=-50)
	#--------------------------------------------------------
	############ wav file loading ##############
	y, sr = librosa.load(wavfile, sr=44100)
	##----------------------------------------


	####### Onset and Tempo detection ##########
	onset = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
	onset_env = librosa.onset.onset_strength(y=y, sr=sr)
	onset_sec = librosa.frames_to_time(onset, sr=sr)
	onset_frames = librosa.frames_to_samples(onset)

	tempo = int(librosa.beat.tempo(onset_envelope=onset_env, sr=sr))
	print(f'Detected Tempo: {tempo}')
	tempo = mido.bpm2tempo(tempo)
	##--------------------------------------------


	#---------grab onset and offset---------------
	beats = onset_offset(sr=sr, onset=onset, onsetframes=onset_frames, silences=silences)

	####### Grabs onset and predicts kick, snare, hihat ############
	predictions = []

	model, class_names = load_model_ext(modelpath)

	for beat in beats:
		current_signal = y[beat[0]:beat[1]]
		pred = predict_one(model, class_names, current_signal, sr)[0]
		predictions.append(pred)
		print(pred)


	##### setup intial midi parameters ########### 
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)

	tick_resolution = 480
	onset_ticks = [int(round(mido.second2tick(x, ticks_per_beat=tick_resolution, tempo=tempo))) for x in onset_sec]
	track.append(mido.MetaMessage('set_tempo', tempo=tempo))

	############## Creates Midi File ##################
	for i, tick in enumerate(onset_ticks):
		previous_tick = 0
		drum_notes = {'kick':36, 'snare':38, 'hihat':42}
		current_note = drum_notes[f'{predictions[i]}']
		if i == 0:
			current_tick = tick
			track.append(Message('note_on', note=current_note, velocity=64, time=current_tick))
			track.append(Message('note_off', note=current_note, time=0))
		else:
			current_tick = tick - onset_ticks[i - 1]
			track.append(Message('note_on', note=current_note, velocity=64, time=current_tick))
			track.append(Message('note_off', note=current_note, time=0))

	mid.save('resources/beatbox.mid')
	K.clear_session()

	return round(mido.tempo2bpm(tempo))
#----------------------------------------------------
#------------------usage-------------------
# audio2midi('resources/output.wav', 'resources/beatbox_model2.hdf5')
