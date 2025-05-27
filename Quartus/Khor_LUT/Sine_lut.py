import numpy as np

with open("sine_lut.hex", "w") as f:
    for i in range(256):
        angle = 2 * np.pi * i / 256
        value = int((np.sin(angle) + 1) * 127.5)
        f.write(f"{value:02X}\n")  # write in hex format
