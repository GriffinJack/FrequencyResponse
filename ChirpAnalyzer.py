import numpy as np
from scipy.signal import chirp
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sounddevice as sd
import os

class ChirpAnalyzer:
    def __init__(self, duration = 1.0, sample_rate= 44100, f0 = 20, f1 = 10000):
        self.time = np.linspace(0, duration, int(duration * sample_rate))
        self.signal = chirp(self.time, f0=f0, f1=f1, t1=duration, method='linear')
        self.sample_rate = sample_rate
        self.duration = duration
        self.wav_path = self.save_as_wav("generated_chirp.wav")
        self.recorded_signal = None
        self.recorded_path = None
        self.response_data = None


    def save_as_wav(self, filename = "chirp.wav"):
        path = os.path.join("static", "wav", filename)
        sig_int16 = np.int16(self.signal/np.max(np.abs(self.signal))*32767)
        write(path, self.sample_rate, sig_int16)
        return path

    def plot_wave(self, filename = "chirp_plot.png", recorded=False, samples=5000):
        path = os.path.join("static", "plots", filename)

        if recorded:
            if self.recorded_signal is None:
                raise ValueError("No recorded signal found. Please run play_wave() first.")
            signal = self.recorded_signal
            label = "Recorded Signal"
        else:
            signal = self.signal
            label = "Generated Chirp"

        plt.figure()
        plt.plot(self.time[:samples], signal[:samples])
        plt.title(f"{label} Waveform")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.savefig(path)

    def play_wave(self, filename = "recorded.wav"):
        print("Playing Waveform")
        recording = sd.playrec(self.signal, self.sample_rate, channels=1, dtype='float32')
        sd.wait()
        print("Done")

        self.recorded_signal = recording.flatten()
        self.recorded_path = os.path.join("static", "wav", filename)

        sig_int16 = np.int16(self.recorded_signal / np.max(np.abs(self.recorded_signal)) * 32767)
        write(self.recorded_path, self.sample_rate, sig_int16)

    def analyze_response(self, plot=True):
        if self.recorded_signal is None:
            raise ValueError("No recorded signal. Run play_wave() first.")

        gen_fft = np.fft.rfft(self.signal)
        rec_fft = np.fft.rfft(self.recorded_signal)

        freqs = np.fft.rfftfreq(int(len(self.signal)), 1 / self.sample_rate)

        gen_mag = np.abs(gen_fft)
        rec_mag = np.abs(rec_fft)

        gen_mag[gen_mag == 0] = 1e-10

        gain_db = 20 * np.log10(rec_mag / gen_mag)

        self.response_data = (freqs, gain_db)

        if plot:
            plt.figure()
            plt.semilogx(freqs, gain_db)
            plt.title("Frequency Response")
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Gain [dB]")
            plt.grid(True, which="both", ls="--", lw=0.5)
            ax = plt.gca()
            ax.set_xscale('log')
            ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
            ax.ticklabel_format(style='plain', axis='x')
            plt.savefig("static/plots/frequency_response.png")
            print("Saved frequency response to static/plots/frequency_response.png")

if __name__ == "__main__":

    sig = ChirpAnalyzer()
    sig.play_wave()
    sig.plot_wave(filename="gen_wave.png")
    sig.plot_wave(filename="recorded_wave.png", recorded=True)
    sig.analyze_response()







