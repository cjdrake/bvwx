"""Test bvwx bitwise operators"""

# pyright: reportArgumentType=false

import pytest

from bvwx import and_, bits, impl, ite, mux, not_, or_, xor

F = bits("1b0")
T = bits("1b1")


def test_not():
    # Array
    x = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    assert str(not_(x)) == "[4b----, 4b0000, 4b1111, 4bXXXX]"
    assert str(~x) == "[4b----, 4b0000, 4b1111, 4bXXXX]"

    # Vec
    x = bits("4b-10X")
    assert not_(x) == bits("4b-01X")
    assert ~x == bits("4b-01X")

    # Scalar
    assert not_(False) == T
    assert not_(0) == T
    assert not_(True) == F
    assert not_(1) == F


def test_or():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(or_(x0, x1)) == "[4b-1-X, 4b111X, 4b-10X, 4bXXXX]"
    assert str(x0 | x1) == "[4b-1-X, 4b111X, 4b-10X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b-1-X_111X_-10X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert or_(v0, x1) == yy
    assert or_(v0, v1) == yy
    assert v0 | x1 == yy
    assert x0 | v1 == yy

    # Int-like inputs
    assert or_(False, False) == F
    assert or_("4b1100", -6) == "4b1110"
    assert bits("4b1100") | -6 == "4b1110"
    assert -6 | bits("4b1100") == "4b1110"
    assert or_("4b1100", 10) == "4b1110"
    assert 10 | bits("4b1100") == "4b1110"

    # Invalid lhs
    with pytest.raises(TypeError):
        or_(42, "4b1010")

    # Invalid rhs
    with pytest.raises(TypeError):
        or_(v0, "1b0")


def test_and():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(and_(x0, x1)) == "[4b--0X, 4b-10X, 4b000X, 4bXXXX]"
    assert str(x0 & x1) == "[4b--0X, 4b-10X, 4b000X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b--0X_-10X_000X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert and_(v0, x1) == yy
    assert and_(v0, v1) == yy
    assert v0 & x1 == yy
    assert x0 & v1 == yy

    # Int-like inputs
    assert and_(False, False) == F
    assert and_("4b1100", -6) == "4b1000"
    assert bits("4b1100") & -6 == "4b1000"
    assert -6 & bits("4b1100") == "4b1000"
    assert and_("4b1100", 10) == "4b1000"
    assert 10 & bits("4b1100") == "4b1000"

    # Invalid rhs
    with pytest.raises(TypeError):
        and_(v0, "1b0")


def test_xor():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(xor(x0, x1)) == "[4b---X, 4b-01X, 4b-10X, 4bXXXX]"
    assert str(x0 ^ x1) == "[4b---X, 4b-01X, 4b-10X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b---X_-01X_-10X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert xor(v0, x1) == yy
    assert xor(v0, v1) == yy
    assert v0 ^ x1 == yy
    assert x0 ^ v1 == yy

    # Int-like inputs
    assert xor(False, False) == F
    assert xor("4b1100", -6) == "4b0110"
    assert bits("4b1100") ^ -6 == "4b0110"
    assert -6 ^ bits("4b1100") == "4b0110"
    assert xor("4b1100", 10) == "4b0110"
    assert 10 ^ bits("4b1100") == "4b0110"

    # Invalid rhs
    with pytest.raises(TypeError):
        xor(v0, "1b0")


def test_impl():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(impl(x0, x1)) == "[4b-1-X, 4b-10X, 4b111X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b-1-X_-10X_111X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert impl(v0, x1) == yy
    assert impl(v0, v1) == yy

    # Int-like inputs
    assert impl(False, False) == T
    assert impl("4b1100", -6) == "4b1011"
    assert impl("4b1100", 10) == "4b1011"

    # Invalid rhs
    with pytest.raises(TypeError):
        impl(v0, "1b0")


ITE = (
    ("1bX", "1bX", "1bX", "1bX"),
    ("1bX", "1bX", "1bX", "1bX"),
    ("1bX", "1bX", "1b1", "1bX"),
    ("1bX", "1bX", "1b0", "1bX"),
    ("1bX", "1bX", "1b-", "1bX"),
    ("1bX", "1b1", "1bX", "1bX"),
    ("1bX", "1b1", "1b1", "1bX"),
    ("1bX", "1b1", "1b0", "1bX"),
    ("1bX", "1b1", "1b-", "1bX"),
    ("1bX", "1b0", "1bX", "1bX"),
    ("1bX", "1b0", "1b1", "1bX"),
    ("1bX", "1b0", "1b0", "1bX"),
    ("1bX", "1b0", "1b-", "1bX"),
    ("1bX", "1b-", "1bX", "1bX"),
    ("1bX", "1b-", "1b1", "1bX"),
    ("1bX", "1b-", "1b0", "1bX"),
    ("1bX", "1b-", "1b-", "1bX"),
    ("1b1", "1bX", "1bX", "1bX"),
    ("1b1", "1bX", "1b1", "1bX"),
    ("1b1", "1bX", "1b0", "1bX"),
    ("1b1", "1bX", "1b-", "1bX"),
    ("1b1", "1b1", "1bX", "1bX"),
    ("1b1", "1b1", "1b1", "1b1"),
    ("1b1", "1b1", "1b0", "1b1"),
    ("1b1", "1b1", "1b-", "1b1"),
    ("1b1", "1b0", "1bX", "1bX"),
    ("1b1", "1b0", "1b1", "1b0"),
    ("1b1", "1b0", "1b0", "1b0"),
    ("1b1", "1b0", "1b-", "1b0"),
    ("1b1", "1b-", "1bX", "1bX"),
    ("1b1", "1b-", "1b1", "1b-"),
    ("1b1", "1b-", "1b0", "1b-"),
    ("1b1", "1b-", "1b-", "1b-"),
    ("1b0", "1bX", "1bX", "1bX"),
    ("1b0", "1bX", "1b1", "1bX"),
    ("1b0", "1bX", "1b0", "1bX"),
    ("1b0", "1bX", "1b-", "1bX"),
    ("1b0", "1b1", "1bX", "1bX"),
    ("1b0", "1b1", "1b1", "1b1"),
    ("1b0", "1b1", "1b0", "1b0"),
    ("1b0", "1b1", "1b-", "1b-"),
    ("1b0", "1b0", "1bX", "1bX"),
    ("1b0", "1b0", "1b1", "1b1"),
    ("1b0", "1b0", "1b0", "1b0"),
    ("1b0", "1b0", "1b-", "1b-"),
    ("1b0", "1b-", "1bX", "1bX"),
    ("1b0", "1b-", "1b1", "1b1"),
    ("1b0", "1b-", "1b0", "1b0"),
    ("1b0", "1b-", "1b-", "1b-"),
    ("1b-", "1bX", "1bX", "1bX"),
    ("1b-", "1bX", "1b1", "1bX"),
    ("1b-", "1bX", "1b0", "1bX"),
    ("1b-", "1bX", "1b-", "1bX"),
    ("1b-", "1b1", "1bX", "1bX"),
    ("1b-", "1b1", "1b1", "1b1"),
    ("1b-", "1b1", "1b0", "1b-"),
    ("1b-", "1b1", "1b-", "1b-"),
    ("1b-", "1b0", "1bX", "1bX"),
    ("1b-", "1b0", "1b1", "1b-"),
    ("1b-", "1b0", "1b0", "1b0"),
    ("1b-", "1b0", "1b-", "1b-"),
    ("1b-", "1b-", "1bX", "1bX"),
    ("1b-", "1b-", "1b1", "1b-"),
    ("1b-", "1b-", "1b0", "1b-"),
    ("1b-", "1b-", "1b-", "1b-"),
    # Int-like inputs
    (False, False, True, T),
    (1, False, True, F),
    (0, "4b1010", "4b0101", "4b0101"),
    (True, "4b1010", "4b0101", "4b1010"),
)


def test_ite():
    for s, a, b, y in ITE:
        assert ite(s, a, b) == y

    with pytest.raises(TypeError):
        assert ite(42, "4b1010", "4b0101")


def test_mux():
    assert mux(bits(), x0="4b1010") == "4b1010"

    assert mux("2b00", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b1000"
    assert mux("2b01", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b1001"
    assert mux("2b10", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b1010"
    assert mux("2b11", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b1011"

    assert mux("2b0-", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b100-"
    assert mux("2b-0", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b10-0"
    assert mux("2b1-", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b101-"
    assert mux("2b-1", x0="4b10_00", x1="4b10_01", x2="4b10_10", x3="4b10_11") == "4b10-1"

    assert mux("2b00", x0="1bX") == "1bX"
    assert mux("2b01", x1="1b0") == "1b0"
    assert mux("2b10", x2="1b1") == "1b1"
    assert mux("2b11", x3="1bW") == "1bW"

    # Int-like inputs
    assert mux(False, x0=False, x1=True) == F
    assert mux(1, x0=False, x1=True) == T
    assert mux(0, x0="4b1010", x1="4b0101") == "4b1010"
    assert mux(True, x0="4b1010", x1="4b0101") == "4b0101"
    assert mux(True, x0="4b1010", x1=5) == "4b0101"
    assert mux(True, x0="4b1010", x1=-1) == "4b1111"

    # Invalid x[n] argument name
    with pytest.raises(ValueError):
        mux("2b00", x4="4b0000")
    with pytest.raises(ValueError):
        mux("2b00", foo="4b0000")
    # Mismatching sizes
    with pytest.raises(TypeError):
        mux("2b00", x0="4b0000", x1="8h00")
    # No inputs
    with pytest.raises(ValueError):
        mux("2b00")
