import numpy as np
import matplotlib.pyplot as plt

# === Parameters ===
n=1
s = 256         # Sampling frequency (Hz)
N = 51         # Number of taps in moving average filter
t = np.linspace(0, 0.0001*n, s*n, endpoint=False)

# === Create a test signal (5 Hz sine + noise) ===
inputSig_float = (5*np.sin(20000*np.pi*t) + 0.41*np.sin(20000*15*np.pi*t + (57/180)*np.pi))
inputSig = np.clip(np.round(((inputSig_float + 5)*255/10)), 0, 255).astype(np.uint8)

# Initialize output signal
outputSig = np.zeros(256, dtype=np.uint8)

# Apply 51-tap moving average
tap_count = 51
for i in range(256):
    if i >= (tap_count - 1):
        window = inputSig[i - (tap_count - 1): i + 1]
        avg = np.sum(window) // tap_count  # Integer division to simulate hardware
        outputSig[i] = avg
    else:
        outputSig[i] = 0  # Zero-padding for first 50 samples

# Plot the result
plt.figure(figsize=(12, 5))
plt.plot(inputSig, label='Original Signal', linestyle='--', alpha=0.7)
plt.plot(outputSig, label='Filtered Output (51-tap MA)', linewidth=2)
plt.title("51-Tap Moving Average Low-Pass Filter")
plt.xlabel("Sample Index")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
