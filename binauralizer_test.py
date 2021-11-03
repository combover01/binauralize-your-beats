import spleeter
import librosa
import ffmpeg
from IPython.display import Audio
import numpy as np
import scipy as sp
import scipy.signal
from scipy.io.wavfile import write

!spleeter separate -p spleeter:4stems -o output/ homage.wav       #### SOURCE SEPARATION: change 'homage.wav' to filename of choice

[stem,sr] = librosa.load('/Users/tuckeralexander/Desktop/spleeter/output/homage/bass.wav')        #### change path
[original,sr] = librosa.load('/Users/tuckeralexander/Desktop/spleeter/homage.wav')                #### change path

def nextpow2(x):
    return int(np.ceil(np.log2(np.abs(x))))            #### for zero padding inside freq_shift function

def freq_shift(x, f_shift, dt):                        #### frequency shifting function
    N_orig = len(x)
    N_padded = 2**nextpow2(N_orig)                     #### zero padding
    t = np.arange(0, N_padded)
    return (scipy.signal.hilbert(np.hstack((x, np.zeros(N_padded-N_orig, x.dtype))))*np.exp(2j*np.pi*f_shift*dt*t))[:N_orig].real

dt = 1/44100
fs = 1/dt
T = 1.0
t = np.arange(0, T, dt)
N = len(t)


def binauralizer(band,gain):           #### creates stereo signal, each channel mixed with original audio for sound quality
    leftear = stem * gain
    leftear = original + leftear
    shift = freq_shift(stem,band,dt)
    rightear = shift * gain
    rightear = original + rightear
    stereo = np.vstack([leftear,rightear])
    stereo = np.transpose(stereo)
    return stereo

#testcase   
stereo=binauralizer(10.0,1)
write("shift.wav",sr,stereo)
