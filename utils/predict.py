from keras.models import load_model
import librosa
import numpy as np
from pydub import AudioSegment
import h5py
from keras import backend as K
import tensorflow as tf

def load_model_ext(filepath, custom_objects=None):
    # global model
    model = load_model(filepath, custom_objects=custom_objects,compile=False)    # load the model normally

    # global graph
    # graph = tf.get_default_graph()
    #--- Now load it again and look for additional useful metadata
    f = h5py.File(filepath, mode='r')

    # initialize class_names with numbers (strings) in case hdf5 file doesn't have any
    output_length = model.layers[-1].output_shape[1]
    class_names = [str(x) for x in range(output_length)]
    if 'class_names' in f.attrs:
        class_names = f.attrs.get('class_names').tolist()
        class_names = [x.decode() for x in class_names]
    f.close()
    return model, class_names

#-------------- Loads Machine Learning Model ---------------------------

# model, class_names = load_model_ext('resources/beatbox_model2.hdf5')

#-----------------------------------------------------------------------

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def predict_one(model, class_names, signal, sr):

    X = make_layered_melgram(signal,sr)
    expected_melgram_shape = model.layers[0].input_shape[1:]

    if (X.shape[1:] != expected_melgram_shape):   # resize if necessary, pad with zeros
        Xnew = np.zeros([1]+list(expected_melgram_shape))
        min1 = min(  Xnew.shape[1], X.shape[1]  )
        min2 = min(  Xnew.shape[2], X.shape[2]  )
        min3 = min(  Xnew.shape[3], X.shape[3]  )
        Xnew[0,:min1,:min2,:min3] = X[0,:min1,:min2,:min3]  # truncate
        X = Xnew
        # with graph.as_default():

        answer = np.argmax(model.predict(X,batch_size=1,verbose=False)[0])
        prob = round((max(model.predict(X,batch_size=1,verbose=False)[0])) * 100)

    return [f"{class_names[answer]}", prob]



# turn multichannel audio as multiple melgram layers
def make_layered_melgram(signal, sr, mels=128, phase=False):
    if (signal.ndim == 1):      # given the way the preprocessing code is  now, this may not get called
        signal = np.reshape( signal, (1,signal.shape[0]))

    # get mel-spectrogram for each channel, and layer them into multi-dim array
    for channel in range(signal.shape[0]):
        melgram = make_melgram(signal[channel],sr, n_mels=mels)

        if (0 == channel):
            layers = melgram
        else:
            layers = np.append(layers,melgram,axis=3)  # we keep axis=0 free for keras batches, axis=3 means 'channels_last'

        if (phase):
            phasegram = make_phase_gram(signal[channel],sr, n_bins=mels)
            layers = np.append(layers,phasegram,axis=3)
    return layers


def make_phase_gram(mono_sig, sr, n_bins=128):
    stft = librosa.stft(mono_sig)#, n_fft = (2*n_bins)-1)
    magnitude, phase = librosa.magphase(stft)   # we don't need magnitude

    # resample the phase array to match n_bins
    phase = np.resize(phase, (n_bins, phase.shape[1]))[np.newaxis,:,:,np.newaxis]
    return phase


def make_melgram(mono_sig, sr, n_mels=128):   # @keunwoochoi upgraded form 96 to 128 mel bins in kapre
    #melgram = librosa.logamplitude(librosa.feature.melspectrogram(mono_sig,  # latest librosa deprecated logamplitude in favor of amplitude_to_db
    #    sr=sr, n_mels=96),ref_power=1.0)[np.newaxis,np.newaxis,:,:]

    melgram = librosa.amplitude_to_db(librosa.feature.melspectrogram(mono_sig,
        sr=sr, n_mels=n_mels))[np.newaxis,:,:,np.newaxis]     # last newaxis is b/c tensorflow wants 'channels_last' order

    '''
    # librosa docs also include a perceptual CQT example:
    CQT = librosa.cqt(mono_sig, sr=sr, fmin=librosa.note_to_hz('A1'))
    freqs = librosa.cqt_frequencies(CQT.shape[0], fmin=librosa.note_to_hz('A1'))
    perceptual_CQT = librosa.perceptual_weighting(CQT**2, freqs, ref=np.max)
    melgram = perceptual_CQT[np.newaxis,np.newaxis,:,:]
    '''
    return melgram