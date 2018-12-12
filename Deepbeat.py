import os
import sys
import time
import threading
import shutil

from Mainwindow import Ui_MainWindow 
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication
from PyQt5.QtMultimedia import QSound, QAudioRecorder, QAudioFormat, QAudioEncoderSettings
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QUrl
import qdarkstyle

# My Classes
from utils.myterrain import Terrain
from utils.midi_player import MidiPlayer
from utils.audio2midi import audio2midi
from utils.metronome import Metronome

import numpy as np
import pyqtgraph as pg
import librosa
from pydub import AudioSegment	

#------------------Embedding files in Pyinstaller Build------------------------------

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)	

#-------------------------------------------------------------------------------

class MainWindow_EXEC():

	def __init__(self):
		
	#-------------------Init QT Setup---------------------------

		app = QtWidgets.QApplication(sys.argv)

		self.MainWindow = QtWidgets.QMainWindow()
		self.ui = Ui_MainWindow()

		self.ui.setupUi(self.MainWindow)   
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

	#------------------Exporting Setup------------------------------

		self.ui.export_midi.clicked.connect(self.openDirectory_midi)
		self.ui.export_midi.setFocusPolicy(QtCore.Qt.NoFocus)
		self.ui.export_audio.clicked.connect(self.openDirectory_audio)
		self.ui.export_audio.setFocusPolicy(QtCore.Qt.NoFocus)


	#------------------Metronome Setup------------------------------

		self.ui.metronome_button.clicked.connect(self.metro_thread)

	#------------------Recording Setup------------------------------

		self.ui.start_stop_rec.clicked.connect(self.start_stop_recording)
		self.ui.play_gui.clicked.connect(self.play)

		# QAudio setup
		self.settings = QAudioEncoderSettings()
		self.settings.setBitRate(16)
		self.settings.setChannelCount(1)
		self.audioRecorder = QAudioRecorder()
		self.audioRecorder.setEncodingSettings(self.settings)
		self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), resource_path("resources/output.wav")))

		self.url = QUrl.fromLocalFile(self.file_path)
		self.audioRecorder.setOutputLocation(self.url)

	#------------------Audio Terrain Gui Setup------------------------------

		self.terrain = Terrain()
		self.terrain.update()	
		self.terrain_widget = self.terrain.getwidget()
		self.layout = QtGui.QGridLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.ui.t_widget.setLayout(self.layout)
		self.layout.addWidget(self.terrain_widget,0,0,1,1)


	#------------------Audio Trimmer Setup------------------------------

		self.ui.audio_trimmer.clicked.connect(self.trim_audio)

		if os.path.isfile("resources/output.wav"):
			self.y, self.sr = librosa.load(resource_path("resources/output.wav"), sr=44100)
		else:
			new_wav = AudioSegment.empty()
			new_wav.export("resources/output.wav", format="wav")
			self.y, self.sr = librosa.load(resource_path("resources/output.wav"), sr=44100)

		self.duration = round(librosa.core.get_duration(y=self.y, sr=self.sr) * self.sr)
		self.maxv = np.iinfo(np.int16).max

		self.win = pg.GraphicsLayoutWidget()
		self.p = self.win.addPlot()

		#removes X & Y Axis and disables mouse movement
		self.p.showAxis('bottom', show=False)
		self.p.showAxis('left', show=False)
		self.p.setMouseEnabled(x=False, y=False)

		self.region = pg.LinearRegionItem(brush=(100, 100, 100, 60),  bounds=(0, self.duration))
		self.region.setRegion([0, self.duration])

		self.p.addItem(self.region, ignoreBounds=True)
		self.p.plot(self.y, pen="w")

		self.layout.addWidget(self.win)
		self.win.hide()



	#------------------Midi Setup------------------------------

		self.ui.convert_midi.clicked.connect(self.convertMidi)
		self.ui.midi_play.clicked.connect(self.midiplayer_thread)
		self.ui.tempo_slider.valueChanged[int].connect(self.tempo_value)
		self.ui.midi_loop.toggle()

		# default bpm is 120
		self.current_tempo = 120
		self.detected_tempo = 120

	#------------------Drum Kit Selector Setup----------------------

		self.ui.drum_kits.clicked.connect(self.select_drumkit)
		self.drum_number = 0
		self.drum_folders = ['Drum_Kit_1','Drum_Kit_2','Drum_Kit_3','Drum_Kit_4']
		self.drum_current = self.drum_folders[self.drum_number]

    #------------------EXEC Window---------------------------------
		self.MainWindow.show()
		sys.exit(app.exec_()) 
    #---------------------------------------------------------------

#------------------Functions----------------------------------

		#------------------Drum Kit Selector------------------------------

	def select_drumkit(self):
		if self.drum_number < 3:
			self.drum_number += 1
			self.drum_current = self.drum_folders[self.drum_number]
			self.ui.drum_kits.setText(self.drum_current.replace("_"," "))
		else:
			self.drum_number = 0
			self.drum_current = self.drum_folders[self.drum_number]
			self.ui.drum_kits.setText(self.drum_current.replace("_"," "))

		#------------------Audio Trimmer------------------------------

	def trim_audio(self):
		# Switch to Trimmer widget 
		self.layout.removeWidget(self.terrain_widget)
		self.terrain_widget.hide()
		self.win.show()
		self.trim_values = self.region.getRegion()
		self.updateaudio()
		# Trims signal array with region values
		self.y = self.y[round(self.trim_values[0]):round(self.trim_values[1])]

		# save the new signal values to wav
		librosa.output.write_wav(resource_path("resources/output.wav"), (self.y * self.maxv).astype(np.int16), self.sr)
		self.updateplot()

	def updateplot(self):
		# Replot the trimmed wav and update region bounds
		self.duration = round(librosa.core.get_duration(y=self.y, sr=self.sr) * self.sr)
		self.p.plot(clear=True)
		self.p.plot(self.y, pen="w")
		self.region = pg.LinearRegionItem(brush=(100, 100, 100, 50),  bounds=(0, self.duration))
		self.p.addItem(self.region, ignoreBounds=True)
		self.region.setRegion([0, self.duration])

	def updateaudio(self):		
		self.y, self.sr = librosa.load(resource_path("resources/output.wav"), sr=44100)

		#------------------Metronome Threading------------------------------
	
	def metro_thread(self):

		if self.ui.metronome_button.isChecked():
			print('metronome is On')
			self.thread = QThread()  # a new thread to run our background tasks in
			self.worker = Worker(self.current_tempo)  # a new worker to perform those tasks
			self.worker.moveToThread(self.thread)  # move the worker into the thread, do this first before connecting the signals
			self.thread.started.connect(self.worker.work)  # begin our worker object's loop when the thread starts running
			self.thread.start()
		
		else:
			print('metronome is Off')
			self.stop_loop()
			self.worker.finished.connect(self.loop_finished) # do something in the gui when the worker loop ends
			self.worker.finished.connect(self.thread.quit)  # tell the thread it's time to stop running
			self.worker.finished.connect(self.thread.wait)
			self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
			self.thread.finished.connect(self.thread.deleteLater) 
	
	def stop_loop(self):
		self.worker.working = False

	def loop_finished(self):
		# print('Worker Finished')
		pass	


	#---------------------------------------------------------


	#------------------ MIDI ------------------------------

	def tempo_value(self, value):
		self.current_tempo = value


	def convertMidi(self):
		self.ui.convert_midi.setEnabled(False)
		self.thread2 = QThread() 
		self.worker2 = ConvertMidi_Worker() 
		self.worker2.moveToThread(self.thread2)  
		self.thread2.started.connect(self.worker2.work)  
		self.thread2.start()
		self.worker2.finished.connect(self.convert_finished)
		self.worker2.finished.connect(self.thread2.quit) 
		self.worker2.finished.connect(self.thread2.wait)
		self.worker2.finished.connect(self.worker2.deleteLater)  
		self.thread2.finished.connect(self.thread2.deleteLater)


	def convert_finished(self,tempo):
		self.detected_tempo = tempo
		self.ui.tempo_slider.setValue(self.detected_tempo)
		self.ui.convert_midi.clearFocus()
		self.ui.convert_midi.setEnabled(True)
		print('Midi Conversion finished')


	def midiplayer_thread(self):

		if self.ui.midi_play.isChecked() and self.ui.midi_loop.isChecked()==False:

			self.ui.midi_play.setEnabled(False)
			self.win.hide()
			self.terrain_widget.show()
			self.terrain.animate()
			self.thread3 = QThread()  
			self.worker3 = MidiPlayer_Worker(self.current_tempo, self.drum_current)  
			self.worker3.moveToThread(self.thread3)  
			self.thread3.started.connect(self.worker3.workonce)  

			self.thread3.start()
			self.worker3.finished2.connect(self.midi_loop_finished2)
			self.worker3.finished2.connect(self.thread3.quit)
			self.worker3.finished2.connect(self.thread3.wait)
			self.worker3.finished2.connect(self.worker3.deleteLater)  
			self.thread3.finished.connect(self.thread3.deleteLater) 


		elif self.ui.midi_play.isChecked() and self.ui.midi_loop.isChecked()==True:
			self.win.hide()
			self.terrain_widget.show()
			self.start_Midi_Thread()
			self.terrain.animate()
			
		elif self.ui.midi_play.isChecked()==False:
			self.terrain.stop_animate()
			self.stop_Midi_Thread()

	def start_Midi_Thread(self):
		self.thread3 = QThread()  
		self.worker3 = MidiPlayer_Worker(self.current_tempo, self.drum_current)
		self.worker3.moveToThread(self.thread3)
		self.thread3.started.connect(self.worker3.work)  
		self.thread3.start()
	

	def stop_Midi_Thread(self):
		self.worker3.working = False

		self.worker3.stop()
		self.worker3.finished.connect(self.midi_loop_finished)
		self.worker3.finished.connect(self.thread3.quit)
		self.worker3.finished.connect(self.thread3.wait)
		self.worker3.finished.connect(self.worker3.deleteLater)
		self.thread3.finished.connect(self.thread3.deleteLater)
		print('done')

	def midi_loop_finished(self):
		print('Midi loop Finished')

	def midi_loop_finished2(self):
		print('Midi Player Finished')
		self.ui.midi_play.toggle()
		self.ui.midi_play.setEnabled(True)
		self.terrain.stop_animate()
	
	#---------------------------------------------------------

	#------------------ Recorder & Player ------------------------------

	def start_stop_recording(self):
		if self.ui.start_stop_rec.isChecked():
			self.ui.play_gui.setEnabled(False)
			self.ui.audio_trimmer.setEnabled(False)

			self.win.hide()
			self.terrain_widget.show()

			self.layout.addWidget(self.terrain_widget)
			self.audioRecorder.record()
			self.terrain.update()

			self.terrain.animate()
			print('Recording...')

		else:
			self.ui.play_gui.setEnabled(True)
			self.ui.audio_trimmer.setEnabled(True)

			self.terrain.stop_animate()
			self.audioRecorder.stop()
			self.layout.removeWidget(self.terrain_widget)
			self.terrain_widget.hide()

			self.updateaudio()
			self.win.show()
			self.updateplot()			
			print('Stop Recording')


	def play(self):
		if self.ui.play_gui.isChecked():
			self.win.hide()
			self.terrain_widget.show()

			self.player = QSound(resource_path("resources/output.wav"))
			self.terrain.animate()
			self.player.play()
			# if self.player.isFinished():
			# 	self.ui.play_gui.toggle()
			# 	print('done')

		else:
			self.terrain.stop_animate()
			self.player.stop()
			self.player.deleteLater()
	
	#------------------ Exporting ------------------------------

	def openDirectory_midi(self):
		self.openDirectoryDialog= QtGui.QFileDialog.getExistingDirectory(self.MainWindow, "Save Midi File")
		if self.openDirectoryDialog:
			self.saveMidi(self.openDirectoryDialog)
		else:
			pass
 
	def openDirectory_audio(self):
		self.openDirectoryDialog= QtGui.QFileDialog.getExistingDirectory(self.MainWindow, "Save Audio File")
		if self.openDirectoryDialog:
			self.saveAudio(self.openDirectoryDialog)
		else:
			pass

	def saveMidi(self, directory):
	    shutil.copy("resources/beatbox.mid", directory)


	def saveAudio(self, directory):
	    shutil.copy("resources/output.wav", directory)

#---------------------------------------------------------------

#----------------- Thread Classes ----------------------------


class Worker(QObject):
	finished = pyqtSignal()

	def __init__(self, bpm):
		super(Worker, self).__init__()
		self.working = True
		self.m = Metronome(bpm)

	def work(self):
		while self.working:			
			self.m.is_playing()
			time.sleep(1)
			
		self.m.stop()
		self.m.end()
		self.finished.emit()

class ConvertMidi_Worker(QObject):
	finished = pyqtSignal(int)

	def __init__(self):
		super(ConvertMidi_Worker, self).__init__()
		self.working = True

	def work(self):
		while self.working:
			self.model = resource_path('resources/beatbox_model2.hdf5')			
			self.detected_tempo = audio2midi(resource_path('resources/output.wav'), self.model)
			self.working = False

		self.finished.emit(self.detected_tempo)

class MidiPlayer_Worker(QObject):
	finished = pyqtSignal()
	finished2 = pyqtSignal()

	def __init__(self, bpm, current_drum_kit):
		super(MidiPlayer_Worker, self).__init__()
		self.current_drum_kit  = current_drum_kit
		self.current_tempo = bpm
		self.working = True
		self.kick = resource_path(f"resources/drumkits/{self.current_drum_kit}/kick.wav")
		self.snare = resource_path(f"resources/drumkits/{self.current_drum_kit}/snare.wav")
		self.hihat = resource_path(f"resources/drumkits/{self.current_drum_kit}/hihat.wav")
		self.mplayer = MidiPlayer(resource_path('resources/beatbox.mid'), self.current_tempo, self.kick, self.snare, self.hihat)

	def work(self):
		self.mplayer.playmidi()
		self.finished.emit()

	def workonce(self):
		while self.working:
			self.mplayer.playonce()
			self.working = False
		self.finished2.emit()

	def stop(self):
		self.mplayer.stopMidi()
        
#---------------------------------------------------------------

if __name__ == "__main__":
    MainWindow_EXEC()

