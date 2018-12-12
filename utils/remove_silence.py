from pydub import AudioSegment, silence	


def remove_silence(wavfile, thresh=-50):
	#Loads wavfile
	song = AudioSegment.from_wav(wavfile)

	#appends small silence to the end of wav incase end of file has nothing undering the threshold
	silence_last = AudioSegment.silent(duration=20)
	song = silence_last + song + silence_last
	#--------------------------------------------------------------------

	silences = silence.detect_silence(song, min_silence_len=20, silence_thresh= thresh)
	length = round(song.duration_seconds *1000)

	#creates empy wav to write into
	new_wav = AudioSegment.empty()
	silence_floor = 50
	silence_tail = 0

	#if no silences detected
	if len(silences) == 0:
		new_wav += song[silence_tail:length]

	#if one silence is detected
	elif len(silences) == 1:
		for s in silences:
			new_wav += song[silence_tail:s[0]]
			new_wav += song[s[0]:s[1]] - silence_floor
			new_wav += song[s[1]:length]

	# more then one silence
	else:
		for s in silences:
			if s != silences[-1]:
				new_wav += song[silence_tail:s[0]]
				new_wav += song[s[0]:s[1]] - silence_floor
				silence_tail = s[1]

			else:
				new_wav += song[silence_tail:s[0]]
				silence_end = (song[s[0]:length]).duration_seconds *1000
				silence_new = AudioSegment.silent(duration=silence_end)
				new_wav += silence_new
	new_wav.export(wavfile, format="wav")
	return silences

## remove_silence('beat.wav',-50)