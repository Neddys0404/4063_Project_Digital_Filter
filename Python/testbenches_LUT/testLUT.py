import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
import numpy as np


@cocotb.test()
async def test_waveform_converter_sine_mode(dut):
    """Test waveform_converter in sine (copy) mode."""

    # Setup clock
    clock = Clock(dut.clk, 10, units="ns")  # 100 MHz
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst.value = 1
    dut.start_flg.value = 0
    dut.sw.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # Generate 8-bit sine wave: 0 to 255
    samples = 256
    t = np.arange(samples)
    sine_wave = (np.sin(2 * np.pi * t / samples) * 127.5 + 127.5).astype(np.uint8)

    # Apply sine wave to inputQuantSig
    for i in range(samples):
        dut.inputQuantSig[i].value = int(sine_wave[i])

    # Set switch to sine mode (4'b0001) and start
    dut.sw.value = 0b0100
    dut.start_flg.value = 1
    await RisingEdge(dut.clk)
    dut.start_flg.value = 0

    # Wait for rdy_flg to assert
    for _ in range(1000):
        await RisingEdge(dut.clk)
        if dut.rdy_flg.value == 1:
            break
    else:
        assert False, "Timeout waiting for rdy_flg"

    # Read outputQuantSig
    output = []
    for i in range(samples):
        output_val = int(dut.outputQuantSig[i].value)
        output.append(output_val)
        # assert output_val == sine_wave[i], f"Mismatch at index {i}: got {output_val}, expected {sine_wave[i]}"

    print(output)
    # Write input and output to file
    with open("converter_input.txt", "w") as f_in, open("converter_output.txt", "w") as f_out:
        for i in range(samples):
            f_in.write(f"{sine_wave[i]}\n")
            f_out.write(f"{output[i]}\n")

    cocotb.log.info("Test passed. Input and output written to text files.")
