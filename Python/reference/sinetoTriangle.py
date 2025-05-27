import numpy as np
import matplotlib.pyplot as plt

# Create a phase-shifted sine wave
samples = 256
x = np.arange(samples)
sine_wave = ((np.sin(2 * np.pi * (x + 40) / samples) + 1) * 127.5).astype(np.uint8)

# Generate triangle wave based on derivative sign
triangle_wave = np.zeros_like(sine_wave, dtype=np.int16)
val = sine_wave[0]

for i in range(samples - 1):
    if (sine_wave[i] >= sine_wave[i + 1]):
        val -= 2  # rising
    else:
        val += 2  # falling
    val = max(0, min(255, val))  # Clamp to 0–255
    triangle_wave[i] = val

triangle_wave[-1] = triangle_wave[-2]

triangle_wave = triangle_wave.astype(np.uint8)

# Plot for comparison
plt.figure(figsize=(10, 4))
plt.plot(x, sine_wave, label='Sine (Shifted)')
plt.plot(x, triangle_wave, '--', label='Triangle (via derivative)')
plt.title("Phase-Aligned Triangle Wave via Derivative")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
