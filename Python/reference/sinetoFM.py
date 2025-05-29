import numpy as np
import matplotlib.pyplot as plt

# Generate an input sine wave (quantized)
samples = 256
x = np.arange(samples)
sine_wave = ((np.sin(2 * np.pi * x / samples) + 1) * 127.5).astype(np.uint8)

# Prepare output buffers
triangle_wave = np.zeros(samples, dtype=np.uint8)
square_wave = np.zeros(samples, dtype=np.uint8)
fm_wave = np.zeros(samples, dtype=np.uint8)

# Triangle wave generation
for i in range(samples):
    if i < 128:
        triangle_wave[i] = i * 2
    else:
        triangle_wave[i] = (255 - i) * 2

# Square wave generation
square_wave = np.where(sine_wave >= 128, 255, 0).astype(np.uint8)

# Corrected Frequency-modulated wave simulation (inverted step size)
pos = 0
fm_bit = 0
for i in range(samples):
    # Map [0, 255] to step sizes [20 (low freq), 1 (high freq)]
    step_size = 51 - (sine_wave[i] * 50) // 255
    pos += 1
    if pos >= step_size:
        fm_bit ^= 1  # Toggle bit
        pos = 0
    fm_wave[i] = 255 if fm_bit else 0

# Plotting all waveforms
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(x, sine_wave, label="Sine Wave")
plt.title("Original Sine Wave (inputQuantSig)")
plt.grid(True)

plt.subplot(4, 1, 2)
plt.plot(x, triangle_wave, label="Triangle Wave", color='orange')
plt.title("Triangle Wave Output")
plt.grid(True)

plt.subplot(4, 1, 3)
plt.plot(x, square_wave, label="Square Wave", color='green')
plt.title("Square Wave Output")
plt.grid(True)

plt.subplot(4, 1, 4)
plt.plot(x, fm_wave, label="Frequency Modulated Wave", color='red')
plt.title("Corrected Frequency Modulated Wave Output (Simulated)")
plt.grid(True)

plt.tight_layout()
plt.show()
