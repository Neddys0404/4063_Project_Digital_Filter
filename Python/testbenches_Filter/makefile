TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES = rtl/moving_avg_filter_51tap.sv
TOPLEVEL = moving_avg_filter_51tap
MODULE = testFir

# For WSL, we'll use Icarus Verilog as it's easy to install
SIM ?= icarus

include $(shell cocotb-config --makefiles)/Makefile.sim