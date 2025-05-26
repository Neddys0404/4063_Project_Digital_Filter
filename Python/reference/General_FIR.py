import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, freqz

# Generate a noisy signal
n = 1 # number of periods
s = 255  # samples per period of signal
t = np.linspace(0, 0.0001*n, s*n, endpoint=False)
signal = (5*np.sin(20000*np.pi*t) + 0.41*np.sin(20000*15*np.pi*t + (57/180)*np.pi))

# FIR filter design
num_taps = 50              # Filter length
cutoff_hz = 10000             # Desired cutoff frequency in Hz
cutoff_norm = 2*np.pi*cutoff_hz / ((s/(0.0001*n)) / 2)  # Normalize to Nyquist

# Design filter using Hamming window
fir_coeff = firwin(numtaps=num_taps, cutoff=cutoff_norm, window='hamming')

# Apply the filter
filtered_signal = lfilter(fir_coeff, 1.0, signal)

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

# Plot frequency response of the filter
w, h = freqz(fir_coeff, worN=8000)
frequencies = w * (s/(0.0001*n)) / (2 * np.pi)

plt.figure()
plt.plot(frequencies, 20 * np.log10(np.abs(h)), 'b')
plt.title("FIR Filter Frequency Response")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True)
plt.axhline(-3, color='r', linestyle='--', label='-3 dB Line')
# plt.axvline(cutoff_hz, color='r', linestyle='--', label=f'Cutoff Frequency ≈ {cutoff_hz:.3f}')
plt.legend()
plt.show()
