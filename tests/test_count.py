"""Test bvwx count operators"""

from bvwx import clz, cpop, ctz, i2bv

CPOP_VALS = [
    ("1b0", "1b0"),
    ("1b1", "1b1"),
    ("1bW", "1bW"),
    ("1bX", "1bX"),
    ("2b00", "2b00"),
    ("2b01", "2b01"),
    ("2b10", "2b01"),
    ("2b11", "2b10"),
    ("3b000", "2b00"),
    ("3b001", "2b01"),
    ("3b010", "2b01"),
    ("3b011", "2b10"),
    ("3b100", "2b01"),
    ("3b101", "2b10"),
    ("3b110", "2b10"),
    ("3b111", "2b11"),
]


def test_cpop():
    for x, y in CPOP_VALS:
        assert cpop(x) == y


CLZ_VALS = [
    ("1b0", "1b1"),
    ("1b1", "1b0"),
    ("1bW", "1bW"),
    ("1bX", "1bX"),
    ("2b00", "2b10"),
    ("2b01", "2b01"),
    ("2b10", "2b00"),
    ("2b11", "2b00"),
    ("3b000", "2b11"),
    ("3b001", "2b10"),
    ("3b010", "2b01"),
    ("3b011", "2b01"),
    ("3b100", "2b00"),
    ("3b101", "2b00"),
    ("3b110", "2b00"),
    ("3b111", "2b00"),
    ("4b0000", "3b100"),
    ("4b0001", "3b011"),
    ("4b0010", "3b010"),
    ("4b0100", "3b001"),
    ("4b1000", "3b000"),
    # Very large numbers
    (i2bv(0, 1024), "11d1024"),
    (i2bv(1, 1024), "11d1023"),
    (i2bv(3, 1024), "11d1022"),
    (i2bv(7, 1024), "11d1021"),
    (i2bv(15, 1024), "11d1020"),
]


def test_clz():
    for x, y in CLZ_VALS:
        assert clz(x) == y


CTZ_VALS = [
    ("1b0", "1b1"),
    ("1b1", "1b0"),
    ("1bW", "1bW"),
    ("1bX", "1bX"),
    ("2b00", "2b10"),
    ("2b01", "2b00"),
    ("2b10", "2b01"),
    ("2b11", "2b00"),
    ("3b000", "2b11"),
    ("3b001", "2b00"),
    ("3b010", "2b01"),
    ("3b011", "2b00"),
    ("3b100", "2b10"),
    ("3b101", "2b00"),
    ("3b110", "2b01"),
    ("3b111", "2b00"),
    ("4b0000", "3b100"),
    ("4b0001", "3b000"),
    ("4b0010", "3b001"),
    ("4b0100", "3b010"),
    ("4b1000", "3b011"),
    # Very large numbers
    (i2bv(0, 1024), "11d1024"),
    (i2bv(-1, 1024), "11d0"),
    (i2bv(-2, 1024), "11d1"),
    (i2bv(-4, 1024), "11d2"),
    (i2bv(-8, 1024), "11d3"),
]


def test_ctz():
    for x, y in CTZ_VALS:
        assert ctz(x) == y
