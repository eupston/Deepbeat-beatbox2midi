import math
import time
import numpy
import pyaudio
import signal
import sys
import argparse
import threading


def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

class Metronome(threading.Thread):
    RATE = 44100
    FREQUENCY = 700
    BPM = 100
    WIDTH = 4
    RAMPUP = .0
    RAMPDOWN = .1
    beat_proportion = .1


    def __init__(self, bpm):


        super(Metronome, self).__init__()

        self.BPM = bpm
        self.subdivide = 1  
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                rate=self.RATE, output=1, stream_callback=lambda a, b, c, d:
                self.populate_stream(a, b, c, d))
        signal.signal(signal.SIGINT, lambda a, b:self.stop())
        self.audio_data = self.generate_metronome_audio() 
        
    def beep(self, frequency, length):
        audio = sine(frequency, length, self.RATE)*.25
        rampup = numpy.arange(int(len(audio)*self.RAMPUP))
        rampup = rampup/len(rampup)
        rampdown= numpy.flip(numpy.arange(int(len(audio)*self.RAMPDOWN)), axis=0)
        rampdown = rampdown/len(rampdown)
        ones = numpy.repeat(1, len(audio) - (len(rampup)+len(rampdown)))
        mask = numpy.append(rampup, ones)
        mask = numpy.append(mask, rampdown)
        audio = numpy.multiply(mask, audio)
        return audio.astype(numpy.float32)

    def generate_metronome_audio(self):
        seconds_per_beat = 1/((self.BPM * self.subdivide)/60)
        audio = self.beep(880,seconds_per_beat*self.beat_proportion)
        audio = numpy.append(audio, numpy.zeros(
            int(seconds_per_beat*(1-self.beat_proportion)*self.RATE)))
        for x in range(self.subdivide-1):
            sub_beep = self.beep(440,seconds_per_beat*self.beat_proportion)
            audio = numpy.append(audio, sub_beep)
            audio = numpy.append(audio, numpy.zeros(
                int(seconds_per_beat*(1-self.beat_proportion)*self.RATE)))
        return audio.astype(numpy.float32)

    def start(self):
        self.index = 0
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()

    def end(self):
        self.stream.close()
        self.p.terminate()

    def populate_stream(self, in_data, frame_count, time_info, status):
        fc = frame_count
        frames = self.audio_data[:0] 
        while (len(frames)!=frame_count):
            frames = numpy.append(frames, self.audio_data[self.index:(self.index+fc)])
            if (self.index+fc) > len(self.audio_data):
                self.index = 0
            else:
                self.index = self.index+fc
            fc = frame_count - len(frames)
        return frames.tobytes(),pyaudio.paContinue 

    def is_playing(self):
        self.start()
        return self.stream.is_active()

# # ------Usage------
# m = Metronome(60)
# m.start()
# while m.is_playing():
#     time.sleep(1)
# m.end()
