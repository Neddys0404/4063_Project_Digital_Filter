import numpy as np
import matplotlib.pyplot as plt

# Generate a noisy signal
n = 1  # number of periods
s = 255  # samples per period of signal
t = np.linspace(0, 0.0001 * n, s * n, endpoint=False)
signal = 5 * np.sin(20000 * np.pi * t) + 0.41 * np.sin(15 * 20000 * np.pi * t + (57 / 180) * np.pi)

# FIR filter design
num_taps = 50 # size of window
cutoff_hz = 10000
fs = s / (0.0001 * n)  # Sampling frequency
cutoff_norm = cutoff_hz / (fs / 2)  # Normalize to Nyquist

# Manually create low-pass filter using sinc function and Hamming window
def sinc_filter(num_taps, cutoff):
    M = num_taps - 1
    h = np.sinc(2 * cutoff * (np.arange(num_taps) - M / 2))
    window = np.hamming(num_taps)
    h *= window
    h /= np.sum(h)
    return h

fir_coeff = sinc_filter(num_taps, cutoff_norm)
print(len(fir_coeff))

# Apply the filter using convolution
filtered_signal = np.convolve(signal, fir_coeff, mode='same')

# Plot time-domain response
plt.figure(figsize=(10, 4))
plt.plot(t, signal, label='Original Signal', alpha=0.5)
plt.plot(t, filtered_signal, label='FIR Filtered Signal', linewidth=2)
plt.title(f"Low-pass FIR Filter ({num_taps} taps, {cutoff_hz} Hz cutoff)")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()

# Frequency response (via FFT)
N = 8000
H = np.fft.fft(fir_coeff, n=N)
frequencies = np.fft.fftfreq(N, d=1/fs)
half = frequencies[:N//2]
magnitude_db = 20 * np.log10(np.abs(H[:N//2]))

plt.figure()
plt.plot(half, magnitude_db, 'b')
plt.title("FIR Filter Frequency Response")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True)
plt.axhline(-3, color='r', linestyle='--', label='-3 dB Line')
plt.legend()
plt.show()
