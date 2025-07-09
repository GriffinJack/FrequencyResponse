import numpy as np
from scipy.signal import chirp
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import sounddevice as sd


def sine_sweep(duration = 1.0, sample_rate = 44100):
    t = np.linspace(0, duration, int(duration * sample_rate))
    signal = chirp(t, f0=20, f1=10000, t1=duration, method='linear')

    return {
        "time": t,
        "signal": signal,
        "sample_rate": sample_rate
        }

def save_as_wav(signal, filename = "chirp.wav", sample_rate = 44100):
    sig_int16 = np.int16(signal/np.max(np.abs(signal))*32767)
    write(filename, sample_rate, sig_int16)

def plot_wave(signal, t, filename):
    plt.figure()
    plt.plot(t[:5000], signal[:5000])
    plt.title("Chirp Waveform")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.savefig(filename)

def play_wave(signal, duration=None):
    if duration is None:
        duration = len(signal['signal']) / signal["sample_rate"]

    print("Playing Waveform")
    recording = sd.playrec(signal['signal'], signal['sample_rate'], channels=1, dtype='float32')
    sd.wait()
    print("Done")
    return {
        "time": signal['time'],
        "signal": recording.flatten(),
        "sample_rate": signal['sample_rate']
    }

if __name__ == "__main__":
    sig = sine_sweep(duration = 0.5)
    save_as_wav(sig["signal"], "testing.wav")
    plot_wave(sig["signal"], sig['time'],"testing.png")

    sample_sig = play_wave(sig, duration = 0.5)
    save_as_wav(sample_sig['signal'], "sample_testing.wav")
    plot_wave(sample_sig["signal"], sample_sig['time'],"sample_testing.png")
    print(sig['signal'].shape)
    print(sample_sig["signal"].shape)







