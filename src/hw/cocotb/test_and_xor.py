import secrets
import sys
from pathlib import Path

import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, Timer

target_dir = Path(__file__).resolve().parent.parent.parent
if str(target_dir) not in sys.path:
    sys.path.append(str(target_dir))
from gf2_mult.gf2_mult import Gf2Mult

PERIOD_NS = 1
gf2_mult = Gf2Mult()
N_RAND = 100
SIM_CYCLES = 3 * N_RAND + 100


async def generate_clock(dut):
    """Generate clock pulses."""

    for _ in range(SIM_CYCLES):
        dut.clk.value = 0
        await Timer(PERIOD_NS / 2, unit="ns")
        dut.clk.value = 1
        await Timer(PERIOD_NS / 2, unit="ns")


@cocotb.test()
async def basic_test(dut):
    """Running Basic Test"""
    cocotb.start_soon(generate_clock(dut))

    await Timer(3, unit="ns")
    await FallingEdge(dut.clk)

    # python model is bit reversed
    x_le = "40000000000000000000000000000000"
    y_le = "40000000000000000000000000000000"
    x_int, y_int, c_int = generate_test_vectors(x_le, y_le)

    dut.i_a.value = x_int
    dut.i_b.value = y_int

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    cocotb.log.info("EXP= %s", hex(c_int))
    cocotb.log.info("ACT= %s", hex(dut.c.value))
    assert dut.c.value == c_int


@cocotb.test()
async def random_test(dut):
    """Running Random Test"""
    cocotb.start_soon(generate_clock(dut))

    await Timer(3, unit="ns")

    for i in range(N_RAND):
        await FallingEdge(dut.clk)

        x_le = secrets.token_hex(16)
        y_le = secrets.token_hex(16)
        x_int, y_int, c_int = generate_test_vectors(x_le, y_le)

        dut.i_a.value = x_int
        dut.i_b.value = y_int

        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)

        cocotb.log.info("x=   %s", hex(x_int))
        cocotb.log.info("y=   %s", hex(y_int))
        cocotb.log.info("EXP= %s", hex(c_int))
        cocotb.log.info("ACT= %s", hex(dut.c.value))
        assert dut.c.value == c_int


def generate_test_vectors(x_le, y_le):
    """python and sv implementations are bit reversed"""
    x_b_le = bytes.fromhex(x_le)
    y_b_le = bytes.fromhex(y_le)
    c_b_le = gf2_mult.bit_parallel(x_b_le, y_b_le)

    x = reverse_hex_bits(x_le)
    y = reverse_hex_bits(y_le)
    x_b = bytes.fromhex(x)
    y_b = bytes.fromhex(y)
    x_int = int.from_bytes(x_b, "big")
    y_int = int.from_bytes(y_b, "big")
    c_b = bytes.fromhex(reverse_hex_bits(c_b_le.hex()))
    c_int = int.from_bytes(c_b, "big")

    return x_int, y_int, c_int


def reverse_hex_bits(hex_str, bit_length=None):
    val = int(hex_str, 16)
    if bit_length is None:
        bit_length = len(hex_str) * 4
    binary = bin(val)[2:].zfill(bit_length)
    reversed_binary = binary[::-1]
    reversed_hex = hex(int(reversed_binary, 2))[2:]
    return reversed_hex.zfill(len(hex_str))
