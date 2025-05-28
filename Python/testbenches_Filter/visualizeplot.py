import matplotlib.pyplot as plt

# Read input signal
with open("./Python/testbenches_Filter/input_signal.txt", "r") as f:
    input_signal = [int(line.strip()) for line in f]

# Read output signal
with open("./Python/testbenches_Filter/output_signal.txt", "r") as f:
    output_signal = [int(line.strip()) for line in f]

# Create time axis
samples = len(input_signal)
time = list(range(samples))

# Plot
plt.figure(figsize=(12, 6))
plt.plot(time, input_signal, label="Input Signal", linestyle='--', marker='o', markersize=3)
plt.plot(time, output_signal, label="Filtered Output", linestyle='-', linewidth=2)
plt.title("FIR Filter Input vs. Output")
plt.xlabel("Sample Index")
plt.ylabel("Signal Value (8-bit)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
