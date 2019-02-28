# Deepbeat-beatbox2midi
Deepbeat converts beatboxing to midi using a Convolutional neural network

# Deepbeat
##### Welcome to the Deepbeat repository!
Deepbeat is a crossplatform application used to convert beatboxing to midi drum information (Kick, Snare, Hihat) using a convolutional neural network trained on 1000s of beatboxing samples. 
It includes an audio recorder and trimmer for recording and slicing your beatboxes. The Midi section includes a convert to midi button, 4 drumkits for midi playback, a looper, tempo slider, and a metronome. Once your happy with your beat simply export the midi and use it in your favourite DAW. A demo of Deepbeat is [here](https://www.youtube.com/watch?v=qxeina_3zQA).


![](resources/images/deepbeat_interface.png)

## Supported Platforms Builds:
- [macOS (Mojave)](https://bit.ly/2zT9LsH)
- [Windows 10](https://bit.ly/2UIAKjm)

## Running from the Terminal
Note this was build using python 3.6 so you'll need this version of python or one that is compatible with pyqt5. Also you'll need to pip install all the modules in `requirements.txt`.

```
cd /deepbeat-beatbox2midi
python Deepbeat.py
```

## Building your own executable
If you'd like to build for a different OS version (particularly Mac) you can use py2app or pyinstaller and the setup files from `Build_setup`.
  
  Windows:
  ```
  pyinstaller deepbeat.spec
  ```
  Mac:
  ```
  python setup.py py2app
  ```
  
##### Special Thanks
This repo uses @Scott Hawley amazing [Panotti](https://github.com/drscotthawley/panotti) for training the beatboxing model. Check it out if you're interested in Audio Classification.

