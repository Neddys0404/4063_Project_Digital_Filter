TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES = rtl/fir_lowpass.sv
TOPLEVEL = fir_lowpass
MODULE = testFir

# For WSL, we'll use Icarus Verilog as it's easy to install
SIM ?= icarus

include $(shell cocotb-config --makefiles)/Makefile.sim