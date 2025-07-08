import numpy as np
from scipy.signal import chirp
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


def sine_sweep(duration = 0.5, sample_rate = 44100):

    t = np.linspace(0, duration, int(duration * sample_rate))

    signal = chirp(t, f0=20, f1=20000, t1=duration, method='linear')

    return signal

def save_as_wav(signal, filename = "chirp.wav", sample_rate = 44100):
    sig_int16 = np.int16(signal/np.max(np.abs(signal))*32767)
    write(filename, sample_rate, sig_int16)










