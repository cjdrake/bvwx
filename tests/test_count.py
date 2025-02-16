"""Test bvwx count operators"""

from bvwx import cpop

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
