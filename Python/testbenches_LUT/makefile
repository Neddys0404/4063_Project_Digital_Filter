TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES = rtl/waveform_converter.sv
TOPLEVEL = waveform_converter
MODULE = testLUT

# For WSL, we'll use Icarus Verilog as it's easy to install
SIM ?= icarus

include $(shell cocotb-config --makefiles)/Makefile.sim