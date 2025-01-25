"""Test Bits methods"""

# For error testing
# pylint: disable=pointless-statement

import pytest

from bvwx import Array, Vec, bits, i2bv, stack, u2bv

E = bits()
T = bits(True)
F = bits(False)


def test_const():
    a = Array[4, 4]
    assert a.shape == (4, 4)

    assert a.xes() == "16bXXXX_XXXX_XXXX_XXXX"
    assert a.zeros() == "16h0000"
    assert a.ones() == "16hFFFF"
    assert a.dcs() == "16b----_----_----_----"

    assert 0 <= a.rand().to_uint() < (1 << 16)


def test_xprop():
    assert Vec[4].xprop(bits("1bX")) == "4bXXXX"
    assert Vec[4].xprop(bits("1b1")) == "4b----"
    assert Vec[4].xprop(bits("1b0")) == "4b----"
    assert Vec[4].xprop(bits("1b-")) == "4b----"


def test_hash():
    s = set()
    s.add(u2bv(0))
    s.add(u2bv(1))
    s.add(u2bv(2))
    s.add(u2bv(3))
    s.add(u2bv(2))
    s.add(u2bv(1))
    s.add(u2bv(0))
    assert len(s) == 4


def test_slicing():
    """Test bits slicing behavior."""
    b = bits(
        [
            ["4b0000", "4b0001", "4b0010", "4b0011"],
            ["4b0100", "4b0101", "4b0110", "4b0111"],
            ["4b1000", "4b1001", "4b1010", "4b1011"],
            ["4b1100", "4b1101", "4b1110", "4b1111"],
        ]
    )

    assert b.shape == (4, 4, 4)

    with pytest.raises(IndexError):
        b[-5]
    with pytest.raises(ValueError):
        b["invalid"]
    # Slice step not supported
    with pytest.raises(ValueError):
        b[0:4:1]

    assert b == b[:]
    assert b == b[0:4]
    assert b == b[-4:]
    assert b == b[-5:]
    assert b == b[:, :]
    assert b == b[:, :, :]

    assert b[0] == b[0, :]
    assert b[0] == b[0, 0:4]
    assert b[0] == b[0, -4:]
    assert b[0] == b[0, -5:]
    assert b[0] == b[0, :, :]

    assert b[0] == bits(["4b0000", "4b0001", "4b0010", "4b0011"])
    assert b[1] == bits(["4b0100", "4b0101", "4b0110", "4b0111"])
    assert b[2] == bits(["4b1000", "4b1001", "4b1010", "4b1011"])
    assert b[3] == bits(["4b1100", "4b1101", "4b1110", "4b1111"])

    assert b[0, 0] == b[0, 0, :]
    assert b[0, 0] == b[0, 0, 0:4]
    assert b[0, 0] == b[0, 0, -4:]
    assert b[0, 0] == b[0, 0, -5:]

    assert b[0, 0] == bits("4b0000")
    assert b[1, 1] == bits("4b0101")
    assert b[2, 2] == bits("4b1010")
    assert b[3, 3] == bits("4b1111")

    assert b[0, :, 0] == bits("4b1010")
    assert b[1, :, 1] == bits("4b1100")
    assert b[2, :, 2] == bits("4b0000")
    assert b[3, :, 3] == bits("4b1111")

    assert b[0, 0, :-1] == bits("3b000")
    assert b[0, 0, :-2] == bits("2b00")
    assert b[0, 0, :-3] == bits("1b0")
    assert b[0, 0, :-4] == bits()

    assert b[0, 0, 0] == F
    # assert b[0, bits("2b00"), 0] == F
    assert b[-4, -4, -4] == F
    assert b[3, 3, 3] == T
    # assert b[3, bits("2b11"), 3] == T
    assert b[-1, -1, -1] == T

    with pytest.raises(ValueError):
        b[0, 0, 0, 0]


def test_vcd():
    assert bits("4b-10X").vcd_var() == "logic"
    assert bits("4b-10X").vcd_val() == "x10x"


def test_count():
    v = bits("8b-10X_-10X")
    assert v.count_xes() == 2
    assert v.count_zeros() == 2
    assert v.count_ones() == 2
    assert v.count_dcs() == 2
    assert v.count_unknown() == 4

    assert not bits("4b0000").onehot()
    assert bits("4b1000").onehot()
    assert bits("4b0001").onehot()
    assert not bits("4b1001").onehot()
    assert not bits("4b1101").onehot()

    assert bits("4b0000").onehot0()
    assert bits("4b1000").onehot0()
    assert not bits("4b1010").onehot0()
    assert not bits("4b1011").onehot0()

    assert not bits("4b0000").has_x()
    assert bits("4b00X0").has_x()
    assert not bits("4b0000").has_dc()
    assert bits("4b00-0").has_dc()
    assert not bits("4b0000").has_unknown()
    assert bits("4b00X0").has_unknown()
    assert bits("4b00-0").has_unknown()


BIN_LITS = {
    "1b0": (1, 0b0),
    "1b1": (1, 0b1),
    "2b00": (2, 0b00),
    "2b01": (2, 0b01),
    "2b10": (2, 0b10),
    "2b11": (2, 0b11),
    "3b100": (3, 0b100),
    "3b101": (3, 0b101),
    "3b110": (3, 0b110),
    "3b111": (3, 0b111),
    "4b1000": (4, 0b1000),
    "4b1001": (4, 0b1001),
    "4b1010": (4, 0b1010),
    "4b1011": (4, 0b1011),
    "4b1100": (4, 0b1100),
    "4b1101": (4, 0b1101),
    "4b1110": (4, 0b1110),
    "4b1111": (4, 0b1111),
    "5b1_0000": (5, 0b1_0000),
    "5b1_1111": (5, 0b1_1111),
    "6b10_0000": (6, 0b10_0000),
    "6b11_1111": (6, 0b11_1111),
    "7b100_0000": (7, 0b100_0000),
    "7b111_1111": (7, 0b111_1111),
    "8b1000_0000": (8, 0b1000_0000),
    "8b1111_1111": (8, 0b1111_1111),
    "9b1_0000_0000": (9, 0b1_0000_0000),
    "9b1_1111_1111": (9, 0b1_1111_1111),
}


def test_lit_bin():
    # Valid inputs w/o X
    for lit, (n, d1) in BIN_LITS.items():
        v = bits(lit)
        assert len(v) == n and v.data[1] == d1

    # Valid inputs w/ X
    v = bits("4b-1_0X")
    assert len(v) == 4 and v.data == (0b1010, 0b1100)
    v = bits("4bX01-")
    assert len(v) == 4 and v.data == (0b0101, 0b0011)

    # Not a literal
    with pytest.raises(ValueError):
        bits("invalid")

    # Size cannot be zero
    with pytest.raises(ValueError):
        bits("0b0")
    # Contains illegal characters
    with pytest.raises(ValueError):
        bits("4b1XW0")

    # Size is too big
    with pytest.raises(ValueError):
        bits("8b1010")

    # Size is too small
    with pytest.raises(ValueError):
        bits("4b1010_1010")


DEC_LITS = {
    "1d0": (1, 0),
    "1d1": (1, 1),
    "2d0": (2, 0),
    "2d1": (2, 1),
    "2d2": (2, 2),
    "2d3": (2, 3),
    "3d4": (3, 4),
    "3d5": (3, 5),
    "3d6": (3, 6),
    "3d7": (3, 7),
    "4d8": (4, 8),
    "4d9": (4, 9),
    "4d10": (4, 10),
    "4d11": (4, 11),
    "4d12": (4, 12),
    "4d13": (4, 13),
    "4d14": (4, 14),
    "4d15": (4, 15),
    "5d16": (5, 16),
    "5d31": (5, 31),
    "6d32": (6, 32),
    "6d63": (6, 63),
    "7d64": (7, 64),
    "7d127": (7, 127),
    "8d128": (8, 128),
    "8d255": (8, 255),
    "9d256": (9, 256),
    "9d511": (9, 511),
}


def test_lit2bv_dec():
    # Valid inputs
    for lit, (n, d1) in DEC_LITS.items():
        v = bits(lit)
        assert len(v) == n and v.data[1] == d1

    # Not a literal
    with pytest.raises(ValueError):
        bits("invalid")

    # Size cannot be zero
    with pytest.raises(ValueError):
        bits("0d0")
    # Contains illegal characters
    with pytest.raises(ValueError):
        bits("8hd3@d_b33f")

    # Size is too small
    with pytest.raises(ValueError):
        bits("8d256")


HEX_LITS = {
    "1h0": (1, 0x0),
    "1h1": (1, 0x1),
    "2h0": (2, 0x0),
    "2h1": (2, 0x1),
    "2h2": (2, 0x2),
    "2h3": (2, 0x3),
    "3h4": (3, 0x4),
    "3h5": (3, 0x5),
    "3h6": (3, 0x6),
    "3h7": (3, 0x7),
    "4h8": (4, 0x8),
    "4h9": (4, 0x9),
    "4hA": (4, 0xA),
    "4hB": (4, 0xB),
    "4hC": (4, 0xC),
    "4hD": (4, 0xD),
    "4hE": (4, 0xE),
    "4hF": (4, 0xF),
    "5h10": (5, 0x10),
    "5h1F": (5, 0x1F),
    "6h20": (6, 0x20),
    "6h3F": (6, 0x3F),
    "7h40": (7, 0x40),
    "7h7F": (7, 0x7F),
    "8h80": (8, 0x80),
    "8hFF": (8, 0xFF),
    "9h100": (9, 0x100),
    "9h1FF": (9, 0x1FF),
}


def test_lit2bv_hex():
    # Valid inputs
    for lit, (n, d1) in HEX_LITS.items():
        v = bits(lit)
        assert len(v) == n and v.data[1] == d1

    # Not a literal
    with pytest.raises(ValueError):
        bits("invalid")

    # Size cannot be zero
    with pytest.raises(ValueError):
        bits("0h0")
    # Contains illegal characters
    with pytest.raises(ValueError):
        bits("8hd3@d_b33f")

    # Size is too small
    with pytest.raises(ValueError):
        bits("8hdead")

    # Invalid characters
    with pytest.raises(ValueError):
        bits("3h8")  # Only 0..7 is legal
    with pytest.raises(ValueError):
        bits("5h20")  # Only 0..1F is legal


U2BV_VALS = {
    0: "[]",
    1: "1b1",
    2: "2b10",
    3: "2b11",
    4: "3b100",
    5: "3b101",
    6: "3b110",
    7: "3b111",
    8: "4b1000",
}

U2BV_N_VALS = {
    (0, 0): "[]",
    (0, 1): "1b0",
    (0, 2): "2b00",
    (1, 1): "1b1",
    (1, 2): "2b01",
    (1, 3): "3b001",
    (1, 4): "4b0001",
    (2, 2): "2b10",
    (2, 3): "3b010",
    (2, 4): "4b0010",
    (3, 2): "2b11",
    (3, 3): "3b011",
    (3, 4): "4b0011",
    (4, 3): "3b100",
    (4, 4): "4b0100",
    (4, 5): "5b0_0100",
}


def test_u2bv():
    # Negative inputs are invalid
    with pytest.raises(ValueError):
        u2bv(-1)

    for i, s in U2BV_VALS.items():
        v = u2bv(i)
        assert str(v) == s
        assert v.to_uint() == i

    for (i, n), s in U2BV_N_VALS.items():
        v = u2bv(i, n)
        assert str(v) == s
        assert v.to_uint() == i

    # Overflows
    with pytest.raises(ValueError):
        u2bv(1, 0)
    with pytest.raises(ValueError):
        u2bv(2, 0)
    with pytest.raises(ValueError):
        u2bv(2, 1)
    with pytest.raises(ValueError):
        u2bv(3, 0)
    with pytest.raises(ValueError):
        u2bv(3, 1)

    with pytest.raises(ValueError):
        bits("4b-10X").to_uint()


I2BV_VALS = {
    -8: "4b1000",
    -7: "4b1001",
    -6: "4b1010",
    -5: "4b1011",
    -4: "3b100",
    -3: "3b101",
    -2: "2b10",
    -1: "1b1",
    0: "1b0",
    1: "2b01",
    2: "3b010",
    3: "3b011",
    4: "4b0100",
    5: "4b0101",
    6: "4b0110",
    7: "4b0111",
    8: "5b0_1000",
}

I2BV_N_VALS = {
    (-5, 4): "4b1011",
    (-5, 5): "5b1_1011",
    (-5, 6): "6b11_1011",
    (-4, 3): "3b100",
    (-4, 4): "4b1100",
    (-4, 5): "5b1_1100",
    (-3, 3): "3b101",
    (-3, 4): "4b1101",
    (-3, 5): "5b1_1101",
    (-2, 2): "2b10",
    (-2, 3): "3b110",
    (-2, 4): "4b1110",
    (-1, 1): "1b1",
    (-1, 2): "2b11",
    (-1, 3): "3b111",
    (0, 1): "1b0",
    (0, 2): "2b00",
    (0, 3): "3b000",
    (1, 2): "2b01",
    (1, 3): "3b001",
    (1, 4): "4b0001",
    (2, 3): "3b010",
    (2, 4): "4b0010",
    (2, 5): "5b0_0010",
    (3, 3): "3b011",
    (3, 4): "4b0011",
    (3, 5): "5b0_0011",
    (4, 4): "4b0100",
    (4, 5): "5b0_0100",
    (4, 6): "6b00_0100",
}


def test_i2bv():
    for i, s in I2BV_VALS.items():
        v = i2bv(i)
        assert str(v) == s
        assert v.to_int() == i
        assert int(v) == i

    for (i, n), s in I2BV_N_VALS.items():
        v = i2bv(i, n)
        assert str(v) == s
        assert v.to_int() == i
        assert int(v) == i

    assert E.to_int() == 0
    assert int(E) == 0

    # Overflows
    with pytest.raises(ValueError):
        i2bv(-5, 3)
    with pytest.raises(ValueError):
        i2bv(-4, 2)
    with pytest.raises(ValueError):
        i2bv(-3, 2)
    with pytest.raises(ValueError):
        i2bv(-2, 1)
    with pytest.raises(ValueError):
        i2bv(-1, 0)
    with pytest.raises(ValueError):
        i2bv(0, 0)
    with pytest.raises(ValueError):
        i2bv(1, 1)
    with pytest.raises(ValueError):
        i2bv(2, 2)
    with pytest.raises(ValueError):
        i2bv(3, 2)
    with pytest.raises(ValueError):
        i2bv(4, 3)

    with pytest.raises(ValueError):
        bits("4b-10X").to_int()


def test_bits():
    assert bits() == E
    assert bits(False) == "1b0"
    assert bits([0, 1, 0, 1]) == "4b1010"
    assert bits(["1b0", "1b1", "1b0", "1b1"]) == "4b1010"
    assert bits(["2b00", "2b01", "2b10", "2b11"]) == "8b11100100"
    assert bits([bits("2b00"), "2b01", "2b10", "2b11"]) == "8b11100100"

    with pytest.raises(TypeError):
        bits(42)
    with pytest.raises(TypeError):
        stack(["2b00", "1b0"])
    with pytest.raises(TypeError):
        stack([0, 0, 0, 42])


def test_stack():
    assert stack() == E
    assert stack(False) == "1b0"
    assert stack(0, 1, 0, 1) == "4b1010"
    assert stack("2b00", "2b01", "2b10", "2b11") == "8b11100100"
    assert stack(bits("2b00"), "2b01", "2b10", "2b11") == "8b11100100"

    with pytest.raises(TypeError):
        stack(42)
    with pytest.raises(TypeError):
        stack("2b00", "1b0")
