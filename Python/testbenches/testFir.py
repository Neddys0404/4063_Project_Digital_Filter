import cocotb
from cocotb.triggers import RisingEdge, Timer
import numpy as np
import matplotlib.pyplot as plt

@cocotb.test()
async def test_fir_lowpass_filter(dut):
    # Clock and reset
    dut.rst.value = 1
    dut.start_flg.value = 0
    await Timer(10, units='ns')
    dut.rst.value = 0

    # Generate 256-sample sine wave scaled to 0–255
    samples = 256
    sine_wave = (np.sin(2 * np.pi * np.arange(samples) / samples) * 127.5 + 127.5).astype(int)

    # Apply the sine wave to inputSig
    for i in range(samples):
        dut.inputSig[i].value = sine_wave[i]

    await Timer(10, units='ns')  # Small delay

    # Start the filtering process
    dut.start_flg.value = 1
    await RisingEdge(dut.clk)
    dut.start_flg.value = 0

    # Wait until rdy_flg is high
    while dut.rdy_flg.value != 1:
        await RisingEdge(dut.clk)

    # Output result
    output = [int(dut.outputSig[i].value) for i in range(samples)]
    print("Filtered Output:", output)

    # Plot input and output signals
    plt.figure(figsize=(10, 4))
    plt.plot(sine_wave, label='Input Sine Wave', linestyle='--')
    plt.plot(output, label='Filtered Output')
    plt.title('FIR Lowpass Filter: Input vs Output')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('fir_filter_output.png')
    plt.show()
