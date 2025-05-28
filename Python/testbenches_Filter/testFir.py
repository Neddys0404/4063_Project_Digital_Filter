import cocotb
from cocotb.triggers import RisingEdge, Timer
import numpy as np
import matplotlib.pyplot as plt

@cocotb.coroutine
async def clock_gen(clk, period_ns):
    """Generate clock pulses."""
    while True:
        clk.value = 0
        await Timer(period_ns / 2, units="ns")
        clk.value = 1
        await Timer(period_ns / 2, units="ns")

import cocotb
from cocotb.triggers import RisingEdge, Timer
import numpy as np

@cocotb.test()
async def test_fir_lowpass_filter(dut):
    """Basic test for FIR low-pass filter"""

    # Constants
    samples = 256
    clk_period_ns = 5  # 100 MHz clock

    # Create a clock
    cocotb.start_soon(clock_gen(dut.clk, clk_period_ns))

    # Reset DUT
    dut.rst.value = 1
    dut.start_flg.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # Generate input signal (sine wave)
    n = 1  # number of periods
    s = 256  # samples per period of signal
    t = np.linspace(0, 0.0001 * n, s * n, endpoint=False)
    inputSig_float = (5 * np.sin(20000 * np.pi * t)) + (0.41 * np.sin(15 * 20000 * np.pi * t + (57 / 180) * np.pi))
    sine_wave = np.clip(np.round(((inputSig_float + 5)*255/10)), 0, 255).astype(np.uint8)

    print(sine_wave)

    # Apply input signal
    for i in range(samples):
        dut.inputSig[i].value = int(sine_wave[i])

    # Trigger filtering
    dut.start_flg.value = 1
    await RisingEdge(dut.clk)
    dut.start_flg.value = 0

    # Wait for rdy_flg
    for _ in range(1000):
        await RisingEdge(dut.clk)
        if dut.rdy_flg.value == 1:
            break
    else:
        assert False, "Timeout: rdy_flg never asserted"

    # Read output
    output = []
    for i in range(samples):
        output.append(int(dut.outputSig[i].value))

    # Print a few values for inspection
    cocotb.log.info(f"Output samples: {output}")

    # visualize
    with open("input_signal.txt", "w") as f:
        for value in sine_wave:
            f.write(f"{value}\n")

    with open("output_signal.txt", "w") as f:
        for value in output:
            f.write(f"{value}\n")
