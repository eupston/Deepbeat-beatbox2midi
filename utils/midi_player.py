import pygame
import mido
from mido import Message, MidiTrack, MidiFile, MetaMessage
import time
import sys

class MidiPlayer():
    # Makes new midi file according to current tempo
    def __init__(self, midi_file, bpm, kick, snare, hihat):
        self.midi_file = midi_file
        self.bpm = bpm
        self.tempo_change()
        print(f'current playing at tempo {self.bpm}')
        self.mid = MidiFile(self.midi_file)
        self.freq = 44100    # audio CD quality
        self.bitsize = -16   # unsigned 16 bit
        self.channels = 1    # 1 is mono, 2 is stereo
        self.buffer = 1024    # number of samples

        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        self.mixer = pygame.mixer
        self.mixer.music.set_volume(1)

        self.kick = self.mixer.Sound(kick)
        self.snare = self.mixer.Sound(snare)
        self.hh = self.mixer.Sound(hihat)

        self.playstate = False
        self.loopstate = False

    def playonce(self):
        self.playstate = True

        for msg in self.mid.play():
            if self.playstate == False:
                break
            else:
                if msg.bytes()[0] == 144:
                    if msg.bytes()[1] == 36:
                        self.kick.play()
                        print('kick')
                    elif msg.bytes()[1] == 38: 
                        self.snare.play()
                        print('snare')
                    elif msg.bytes()[1] == 42: 
                        self.hh.play()
                        print('hihat')
                    else:        
                        pass


    def playmidi(self):

        self.playstate = True
        while self.playstate:
            for msg in self.mid.play():
                current_note = msg.bytes()[1]

                if self.playstate == False:
                    break
                else:
                    if msg.bytes()[0] == 144:
                        if msg.bytes()[1] == 36:
                            self.kick.play()
                            print('kick')
                        elif msg.bytes()[1] == 38: 
                            self.snare.play()
                            print('snare')
                        elif msg.bytes()[1] == 42: 
                            self.hh.play()
                            print('hihat')
                        else:        
                            pass

    def tempo_change(self):

        mid = MidiFile(self.midi_file)
        mid_new = MidiFile()
        track = MidiTrack()
        mid_new.tracks.append(track)

        bpm = self.bpm
        tempo_new = mido.bpm2tempo(bpm)
        track.append(MetaMessage('set_tempo', tempo=tempo_new))

        for t in mid.tracks:
            for msg in t:
                if msg.type == 'note_on':
                    track.append(Message('note_on', note=msg.note, velocity=msg.note, time=msg.time))
                elif msg.type == 'note_off':
                    track.append(Message('note_off', note=msg.note, time=msg.time))

        mid_new.save(self.midi_file)

    def stopMidi(self):
        self.playstate = False

