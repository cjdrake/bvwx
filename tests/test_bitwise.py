"""Test bvwx bitwise operators"""

import pytest

from bvwx import and_, bits, impl, ite, mux, nand, nor, not_, or_, xnor, xor


def test_not():
    # Array
    x = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    assert str(not_(x)) == "[4b----, 4b0000, 4b1111, 4bXXXX]"
    assert str(~x) == "[4b----, 4b0000, 4b1111, 4bXXXX]"

    # Vec
    x = bits("4b-10X")
    assert not_(x) == bits("4b-01X")
    assert ~x == bits("4b-01X")


def test_nor():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(nor(x0, x1)) == "[4b-0-X, 4b000X, 4b-01X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b-0-X_000X_-01X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert nor(v0, x1) == yy
    assert nor(v0, v1) == yy
    assert ~(v0 | x1) == yy
    assert ~(x0 | v1) == yy

    # Invalid rhs
    with pytest.raises(TypeError):
        nor(v0, "1b0")


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

    # Invalid rhs
    with pytest.raises(TypeError):
        or_(v0, "1b0")


def test_nand():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(nand(x0, x1)) == "[4b--1X, 4b-01X, 4b111X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b--1X_-01X_111X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert nand(v0, x1) == yy
    assert nand(v0, v1) == yy
    assert ~(v0 & x1) == yy
    assert ~(x0 & v1) == yy

    # Invalid rhs
    with pytest.raises(TypeError):
        nand(v0, "1b0")


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

    # Invalid rhs
    with pytest.raises(TypeError):
        and_(v0, "1b0")


def test_xnor():
    # Array
    x0 = bits(["4b----", "4b1111", "4b0000", "4bXXXX"])
    x1 = bits(["4b-10X", "4b-10X", "4b-10X", "4b-10X"])
    assert str(xnor(x0, x1)) == "[4b---X, 4b-10X, 4b-01X, 4bXXXX]"

    # Vec
    x0 = "16b----_1111_0000_XXXX"
    x1 = "16b-10X_-10X_-10X_-10X"
    yy = "16b---X_-10X_-01X_XXXX"
    v0 = bits(x0)
    v1 = bits(x1)

    assert xnor(v0, x1) == yy
    assert xnor(v0, v1) == yy
    assert ~(v0 ^ x1) == yy
    assert ~(x0 ^ v1) == yy

    # Invalid rhs
    with pytest.raises(TypeError):
        xnor(v0, "1b0")


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
)


def test_ite():
    for s, a, b, y in ITE:
        assert ite(s, a, b) == y


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
