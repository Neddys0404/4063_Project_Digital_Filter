import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

# === Parameters ===
n=1
s = 256        # Sampling frequency (Hz)
N = 51         # Number of taps in moving average filter
t = np.linspace(0, 0.0001*n, s*n, endpoint=False)

# === Create a test signal (5 Hz sine + noise) ===
signal = (5*np.sin(20000*np.pi*t) + 0.41*np.sin(20000*15*np.pi*t + (57/180)*np.pi))

# === Design Moving Average Filter ===
kernel = np.ones(N) / N  # Averaging kernel
filtered_signal = np.convolve(signal, kernel, mode='same')

# === Plot Time-Domain Signal ===
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label='Original Signal', alpha=0.5)
plt.plot(t, filtered_signal, label=f'{N}-Point Moving Average', linewidth=2)
plt.title(f"{N}-Point Moving Average Filter - Time Domain")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Frequency Response of Moving Average Filter ===
w, h = freqz(kernel, worN=8000)
frequencies = w * (s/(0.0001*n)) / (2 * np.pi)  # Normalized frequency (0 to 0.5)

# Approximate cutoff frequency
fc_norm = 0.443 * (s/(0.0001*n)) / N

# === Plot Frequency Response ===
plt.figure(figsize=(8, 4))
plt.plot(frequencies, 20 * np.log10(np.abs(h)), 'b')
plt.axvline(fc_norm, color='g', linestyle='--', label=f'Approx. Cutoff ≈ {fc_norm:.3f}')
plt.title(f"Frequency Response of {N}-Point Moving Average Filter")
plt.xlabel("Normalized Frequency (× Nyquist)")
plt.ylabel("Magnitude [dB]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
