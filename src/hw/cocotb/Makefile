# uv run make
# Verilator runs out of memory and crashes for large combinational logic

# SIM ?= verilator
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/../and_xor.sv
COCOTB_TOPLEVEL = and_xor
COCOTB_TEST_MODULES = test_and_xor
include $(shell cocotb-config --makefiles)/Makefile.sim
