import numpy as np
import matplotlib.pyplot as plt

# Original floating-point coefficients
float_coeffs = np.array([
    0.00242698, 0.00259684, 0.00300694, 0.00366492, 0.00457305, 0.00572802,
    0.00712089, 0.00873714, 0.01055687, 0.01255514, 0.01470241, 0.01696509,
    0.01930626, 0.02168639, 0.02406419, 0.02639746, 0.02864405, 0.03076275,
    0.0327142,  0.03446178, 0.0359724,  0.03721727, 0.03817254, 0.03881982,
    0.03914661, 0.03914661, 0.03881982, 0.03817254, 0.03721727, 0.0359724,
    0.03446178, 0.0327142,  0.03076275, 0.02864405, 0.02639746, 0.02406419,
    0.02168639, 0.01930626, 0.01696509, 0.01470241, 0.01255514, 0.01055687,
    0.00873714, 0.00712089, 0.00572802, 0.00457305, 0.00366492, 0.00300694,
    0.00259684, 0.00242698
])

# Convert to Q2.14 fixed-point
FRAC_BITS = 14
q_coeffs = np.round(float_coeffs * (1 << FRAC_BITS)).astype(np.int16)

# Generate sine wave input (0–255 range)
n = 10  # number of periods
s = 256  # samples per period of signal
N = s * n
t = np.linspace(0, 0.0001 * n, N, endpoint=False)
inputSig_float = 5 * np.sin(20000 * np.pi * t) + 0.41 * np.sin(15 * 20000 * np.pi * t + (57 / 180) * np.pi)
inputSig = np.clip(np.round(((inputSig_float + 5)*255/10)), 0, 255).astype(np.uint8)

# Apply fixed-point FIR filtering
outputSig = np.zeros(N, dtype=np.uint8)
for i in range(N):
    acc = 0
    for j in range(len(q_coeffs)):
        if i - j >= 0:
            acc += int(inputSig[i - j]) * int(q_coeffs[j])
    acc_shifted = acc >> FRAC_BITS
    acc_clamped = min(max(acc_shifted, 0), 255)
    outputSig[i] = acc_clamped

# Plot
plt.figure(figsize=(10, 4))
plt.plot(inputSig, label='Input Sine Wave', linestyle='--', color='gray')
plt.plot(outputSig, label='Filtered Output', linewidth=2, color='blue')
plt.title('Fixed-Point FIR Filter on Sine Wave Input')
plt.xlabel('Sample Index')
plt.ylabel('Signal Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
