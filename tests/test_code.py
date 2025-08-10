"""Test bvwx encode/decode operators."""

import pytest

from bvwx import bits, decode, encode_onehot, encode_priority

E = bits()


ENC_OH_VALS = [
    ("1b1", E),
    ("2b01", "1b0"),
    ("2b10", "1b1"),
    ("3b001", "2b00"),
    ("3b010", "2b01"),
    ("3b100", "2b10"),
    ("4b0001", "2b00"),
    ("4b0010", "2b01"),
    ("4b0100", "2b10"),
    ("4b1000", "2b11"),
    ("2b--", "1b-"),
    ("2bXX", "1bX"),
]


def test_encode_onehot():
    # Not a valid one-hot encoding
    with pytest.raises(ValueError):
        encode_onehot("1b0")
    with pytest.raises(ValueError):
        encode_onehot("2b00")

    for x, y in ENC_OH_VALS:
        assert y == encode_onehot(x)


ENC_PRI_VALS = [
    ("1b0", (E, "1b0")),
    ("1b1", (E, "1b1")),
    ("2b00", ("1b-", "1b0")),
    ("2b01", ("1b0", "1b1")),
    ("2b10", ("1b1", "1b1")),
    ("2b11", ("1b1", "1b1")),
    ("3b000", ("2b--", "1b0")),
    ("3b001", ("2b00", "1b1")),
    ("3b010", ("2b01", "1b1")),
    ("3b011", ("2b01", "1b1")),
    ("3b100", ("2b10", "1b1")),
    ("3b101", ("2b10", "1b1")),
    ("3b110", ("2b10", "1b1")),
    ("3b111", ("2b10", "1b1")),
    ("4b0000", ("2b--", "1b0")),
    ("4b0001", ("2b00", "1b1")),
    ("4b0010", ("2b01", "1b1")),
    ("4b0011", ("2b01", "1b1")),
    ("4b001-", ("2b01", "1b1")),
    ("4b0100", ("2b10", "1b1")),
    ("4b0101", ("2b10", "1b1")),
    ("4b0110", ("2b10", "1b1")),
    ("4b0111", ("2b10", "1b1")),
    ("4b01--", ("2b10", "1b1")),
    ("4b1000", ("2b11", "1b1")),
    ("4b1001", ("2b11", "1b1")),
    ("4b1010", ("2b11", "1b1")),
    ("4b1011", ("2b11", "1b1")),
    ("4b1100", ("2b11", "1b1")),
    ("4b1101", ("2b11", "1b1")),
    ("4b1110", ("2b11", "1b1")),
    ("4b1111", ("2b11", "1b1")),
    ("4b1---", ("2b11", "1b1")),
    # DC Propagation
    ("1b-", (E, "1b-")),
    ("2b--", ("1b-", "1b-")),
    ("2b0-", ("1b-", "1b-")),
    ("3b---", ("2b--", "1b-")),
    ("3b0--", ("2b--", "1b-")),
    ("3b00-", ("2b--", "1b-")),
    ("4b----", ("2b--", "1b-")),
    ("4b0---", ("2b--", "1b-")),
    ("4b00--", ("2b--", "1b-")),
    ("4b000-", ("2b--", "1b-")),
    # X Propagation
    ("2bXX", ("1bX", "1bX")),
    ("3b10X", ("2bXX", "1bX")),
]


def test_encode_priority():
    for x, y in ENC_PRI_VALS:
        assert y == encode_priority(x)


DEC_VALS = [
    (E, "1b1"),
    ("1b0", "2b01"),
    ("1b1", "2b10"),
    ("2b00", "4b0001"),
    ("2b01", "4b0010"),
    ("2b10", "4b0100"),
    ("2b11", "4b1000"),
    ("1b-", "2b--"),
    ("1bX", "2bXX"),
]


def test_decode():
    for x, y in DEC_VALS:
        assert y == decode(x)
