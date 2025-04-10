"""Test bvwx arithmetic operators"""

import pytest

from bvwx import adc, add, bits, cat, div, lsh, matmul, mod, mul, neg, ngc, rsh, sbc, srsh, sub

E = bits()

F = bits(False)
T = bits(True)
W = bits("1b-")
X = bits("1bX")


ADD_VALS = [
    ("2b00", "2b00", "1b0", "2b00", F),
    ("2b00", "2b01", "1b0", "2b01", F),
    ("2b00", "2b10", "1b0", "2b10", F),
    ("2b00", "2b11", "1b0", "2b11", F),
    ("2b01", "2b00", "1b0", "2b01", F),
    ("2b01", "2b01", "1b0", "2b10", F),  # overflow
    ("2b01", "2b10", "1b0", "2b11", F),
    ("2b01", "2b11", "1b0", "2b00", T),
    ("2b10", "2b00", "1b0", "2b10", F),
    ("2b10", "2b01", "1b0", "2b11", F),
    ("2b10", "2b10", "1b0", "2b00", T),  # overflow
    ("2b10", "2b11", "1b0", "2b01", T),  # overflow
    ("2b11", "2b00", "1b0", "2b11", F),
    ("2b11", "2b01", "1b0", "2b00", T),
    ("2b11", "2b10", "1b0", "2b01", T),  # overflow
    ("2b11", "2b11", "1b0", "2b10", T),
    ("2b00", "2b00", "1b1", "2b01", F),
    ("2b00", "2b01", "1b1", "2b10", F),  # overflow
    ("2b00", "2b10", "1b1", "2b11", F),
    ("2b00", "2b11", "1b1", "2b00", T),
    ("2b01", "2b00", "1b1", "2b10", F),  # overflow
    ("2b01", "2b01", "1b1", "2b11", F),  # overflow
    ("2b01", "2b10", "1b1", "2b00", T),
    ("2b01", "2b11", "1b1", "2b01", T),
    ("2b10", "2b00", "1b1", "2b11", F),
    ("2b10", "2b01", "1b1", "2b00", T),
    ("2b10", "2b10", "1b1", "2b01", T),  # overflow
    ("2b10", "2b11", "1b1", "2b10", T),
    ("2b11", "2b00", "1b1", "2b00", T),
    ("2b11", "2b01", "1b1", "2b01", T),
    ("2b11", "2b10", "1b1", "2b10", T),
    ("2b11", "2b11", "1b1", "2b11", T),
    ("2b0X", "2b00", F, "2bXX", X),
    ("2b00", "2b0X", F, "2bXX", X),
    ("2b00", "2b00", X, "2bXX", X),
    ("2b0-", "2b00", F, "2b--", W),
    ("2b00", "2b0-", F, "2b--", W),
    ("2b00", "2b00", W, "2b--", W),
    # Mismatched sizes
    ("2b01", "3b001", F, "3b010", F),
    ("3b001", "2b01", F, "3b010", F),
    # Allow bool inputs
    (False, False, False, "1b0", F),
    (False, False, True, "1b1", F),
    (False, True, False, "1b1", F),
    (False, True, True, "1b0", T),
    (True, False, False, "1b1", F),
    (True, False, True, "1b0", T),
    (True, True, False, "1b0", T),
    (True, True, True, "1b1", T),
]


def test_add():
    """Test bits add method."""
    for a, b, ci, s, co in ADD_VALS:
        assert adc(a, b, ci) == cat(s, co)
        assert add(a, b, ci) == s
        if ci == F:
            assert bits(a) + b == cat(s, co)
            assert a + bits(b) == cat(s, co)


def test_inc_unknown():
    assert -bits("1bX") == bits("2bXX")
    assert -bits("1b-") == bits("2b--")


def test_array_add():
    a = bits(["4b1010", "4b0101"])
    b = bits(["4b0101", "4b1010"])
    assert str(adc(a, b)) == "9b0_1111_1111"
    assert str(add(a, b)) == "[4b1111, 4b1111]"


SUB_VALS = [
    ("2b00", "2b00", "2b00", T),
    ("2b00", "2b01", "2b11", F),
    ("2b00", "2b10", "2b10", F),
    ("2b00", "2b11", "2b01", F),
    ("2b01", "2b00", "2b01", T),
    ("2b01", "2b01", "2b00", T),
    ("2b01", "2b10", "2b11", F),
    ("2b01", "2b11", "2b10", F),
    ("2b10", "2b00", "2b10", T),
    ("2b10", "2b01", "2b01", T),
    ("2b10", "2b10", "2b00", T),
    ("2b10", "2b11", "2b11", F),
    ("2b11", "2b00", "2b11", T),
    ("2b11", "2b01", "2b10", T),
    ("2b11", "2b10", "2b01", T),
    ("2b11", "2b11", "2b00", T),
    ("2b0X", "2b00", "2bXX", X),
    ("2b00", "2b0X", "2bXX", X),
    ("2b0-", "2b00", "2b--", W),
    ("2b00", "2b0-", "2b--", W),
]


def test_sub():
    for a, b, s, co in SUB_VALS:
        assert sbc(a, b) == cat(s, co)
        assert sub(a, b) == s
        assert bits(a) - b == cat(s, co)
        assert a - bits(b) == cat(s, co)


def test_array_sub():
    a = bits(["4b1111", "4b1111"])
    b = bits(["4b0101", "4b1010"])
    assert str(sbc(a, b)) == "9b1_0101_1010"
    assert str(sub(a, b)) == "[4b1010, 4b0101]"


NEG_VALS = [
    ("3b000", "3b000"),
    ("3b001", "3b111"),
    ("3b111", "3b001"),
    ("3b010", "3b110"),
    ("3b110", "3b010"),
    ("3b011", "3b101"),
    ("3b101", "3b011"),
    ("3b100", "3b100"),
]


def test_neg():
    for a, s in NEG_VALS:
        assert neg(a) == s


NGC_VALS = [
    ("3b000", "4b1000"),
    ("3b001", "4b0111"),
    ("3b111", "4b0001"),
    ("3b010", "4b0110"),
    ("3b110", "4b0010"),
    ("3b011", "4b0101"),
    ("3b101", "4b0011"),
    ("3b100", "4b0100"),
]


def test_ngc():
    for a, s in NGC_VALS:
        assert ngc(a) == s
        assert -bits(a) == s


MUL_VALS = [
    ("1b0", "1b0", "2b00"),
    ("1b0", "1b1", "2b00"),
    ("1b1", "1b0", "2b00"),
    ("1b1", "1b1", "2b01"),
    ("2b00", "2b00", "4b0000"),
    ("2b00", "2b01", "4b0000"),
    ("2b00", "2b10", "4b0000"),
    ("2b00", "2b11", "4b0000"),
    ("2b01", "2b00", "4b0000"),
    ("2b01", "2b01", "4b0001"),
    ("2b01", "2b10", "4b0010"),
    ("2b01", "2b11", "4b0011"),
    ("2b10", "2b00", "4b0000"),
    ("2b10", "2b01", "4b0010"),
    ("2b10", "2b10", "4b0100"),
    ("2b10", "2b11", "4b0110"),
    ("2b11", "2b00", "4b0000"),
    ("2b11", "2b01", "4b0011"),
    ("2b11", "2b10", "4b0110"),
    ("2b11", "2b11", "4b1001"),
    ("2b0X", "2b00", "4bXXXX"),
    ("2b0-", "2b00", "4b----"),
]


def test_mul():
    # Empty X Empty = Empty
    assert mul(E, E) == E

    for a, b, p in MUL_VALS:
        assert mul(a, b) == p
        assert bits(a) * b == p
        assert a * bits(b) == p


DIV_VALS = [
    ("1b0", "1b1", "1b0"),
    ("1b1", "1b1", "1b1"),
    ("8d42", "8d7", "8d6"),
    ("8d42", "8d6", "8d7"),
    ("8d42", "4d6", "8d7"),
    ("8d42", "8d8", "8d5"),
    ("8d42", "8d9", "8d4"),
    ("8d42", "8d10", "8d4"),
    ("8d42", "4bXXXX", "8bXXXX_XXXX"),
    ("8d42", "4b----", "8b----_----"),
]


def test_div():
    # Cannot divide by empty
    with pytest.raises(ValueError):
        div("2b00", E)
    # Cannot divide by zero
    with pytest.raises(ZeroDivisionError):
        div("8d42", "8d0")
    # Divisor cannot be wider than dividend
    with pytest.raises(ValueError):
        div("2b00", "8d42")

    for a, b, q in DIV_VALS:
        assert div(a, b) == q
        assert bits(a) // b == q
        assert a // bits(b) == q


MOD_VALS = [
    ("1b0", "1b1", "1b0"),
    ("1b1", "1b1", "1b0"),
    ("8d42", "8d7", "8d0"),
    ("8d42", "8d6", "8d0"),
    ("8d42", "4d6", "4d0"),
    ("8d42", "8d8", "8d2"),
    ("8d42", "8d9", "8d6"),
    ("8d42", "8d10", "8d2"),
    ("8d42", "4bXXXX", "4bXXXX"),
    ("8d42", "4b----", "4b----"),
]


def test_mod():
    # Cannot divide by empty
    with pytest.raises(ValueError):
        mod("2b00", E)
    # Cannot divide by zero
    with pytest.raises(ZeroDivisionError):
        mod("8d42", "8d0")
    # Divisor cannot be wider than dividend
    with pytest.raises(ValueError):
        mod("2b00", "8d42")

    for a, b, r in MOD_VALS:
        assert mod(a, b) == r
        assert bits(a) % b == r


def test_lsh():
    v = bits("4b1111")
    y = lsh(v, 0)
    assert y is v
    assert lsh(v, 1) == "4b1110"
    assert lsh(v, 2) == "4b1100"
    assert v << 2 == "4b1100"
    assert "4b1111" << bits("2b10") == "4b1100"
    assert bits("4b1111") << "2b10" == "4b1100"
    assert bits("4b1111") << bits("2b10") == "4b1100"
    assert lsh(v, 3) == "4b1000"
    assert lsh(v, 4) == "4b0000"

    with pytest.raises(ValueError):
        lsh(v, -1)
    with pytest.raises(ValueError):
        lsh(v, 5)
    with pytest.raises(TypeError):
        lsh(v, 0.5)

    assert lsh("2b01", "1bX") == bits("2bXX")
    assert lsh("2b01", "1b-") == bits("2b--")
    assert lsh("2b01", "1b1") == bits("2b10")


def test_array_lsh():
    x = bits(["4b1111", "4b0000"])
    assert str(x << 2) == "[4b1100, 4b0011]"


def test_rsh():
    v = bits("4b1111")
    y = rsh(v, 0)
    assert y is v
    assert rsh(v, 1) == "4b0111"
    assert rsh(v, 2) == "4b0011"
    assert v >> 2 == "4b0011"
    assert "4b1111" >> bits("2b10") == "4b0011"
    assert bits("4b1111") >> "2b10" == "4b0011"
    assert bits("4b1111") >> bits("2b10") == "4b0011"
    assert rsh(v, 3) == "4b0001"
    assert rsh(v, 4) == "4b0000"

    with pytest.raises(ValueError):
        rsh(v, -1)
    with pytest.raises(ValueError):
        rsh(v, 5)

    assert rsh("2b01", "1bX") == bits("2bXX")
    assert rsh("2b01", "1b-") == bits("2b--")
    assert rsh("2b01", "1b1") == bits("2b00")


def test_array_rsh():
    x = bits(["4b1111", "4b0000"])
    assert str(x >> 2) == "[4b0011, 4b0000]"


def test_srsh():
    v = bits("4b1111")
    assert srsh(v, 0) == "4b1111"
    assert srsh(v, 1) == "4b1111"
    assert srsh(v, 2) == "4b1111"
    assert srsh(v, 3) == "4b1111"
    assert srsh(v, 4) == "4b1111"

    v = bits("4b0111")
    assert srsh(v, 0) == "4b0111"
    assert srsh(v, 1) == "4b0011"
    assert srsh(v, 2) == "4b0001"
    assert srsh(v, 3) == "4b0000"
    assert srsh(v, 4) == "4b0000"

    with pytest.raises(ValueError):
        srsh(v, -1)
    with pytest.raises(ValueError):
        srsh(v, 5)

    assert srsh("2b01", "1bX") == bits("2bXX")
    assert srsh("2b01", "1b-") == bits("2b--")
    assert srsh("2b01", "1b1") == bits("2b00")


def test_array_srsh():
    x = bits(["4b1111", "4b0000"])
    y = srsh(x, 2)
    assert str(y) == "[4b0011, 4b0000]"

    x = bits(["4b0000", "4b1111"])
    y = srsh(x, 2)
    assert str(y) == "[4b1100, 4b1111]"


VECMUL_VALS = [
    # Vec[n] X Vec[n] => Scalar
    ("2b00", "2b00", "1b0"),
    ("2b00", "2b01", "1b0"),
    ("2b00", "2b10", "1b0"),
    ("2b00", "2b11", "1b0"),
    ("2b01", "2b00", "1b0"),
    ("2b01", "2b01", "1b1"),
    ("2b01", "2b10", "1b0"),
    ("2b01", "2b11", "1b1"),
    ("2b10", "2b00", "1b0"),
    ("2b10", "2b01", "1b0"),
    ("2b10", "2b10", "1b1"),
    ("2b10", "2b11", "1b1"),
    ("2b11", "2b00", "1b0"),
    ("2b11", "2b01", "1b1"),
    ("2b11", "2b10", "1b1"),
    ("2b11", "2b11", "1b1"),
]

MATMUL_VALS = [
    # Vec[m] X Array[m,n] => Vec[n]
    ("2b00", ["4b1100", "4b1010"], "4b0000"),
    ("2b01", ["4b1100", "4b1010"], "4b1100"),
    ("2b10", ["4b1100", "4b1010"], "4b1010"),
    ("2b11", ["4b1100", "4b1010"], "4b1110"),
    # Array[m,n] X Vec[n] => Vec[m]
    (["2b00", "2b01", "2b10", "2b11"], "2b00", "4b0000"),
    (["2b00", "2b01", "2b10", "2b11"], "2b01", "4b1010"),
    (["2b00", "2b01", "2b10", "2b11"], "2b10", "4b1100"),
    (["2b00", "2b01", "2b10", "2b11"], "2b11", "4b1110"),
    # Array[m,n] X Array[n,p] => Array[m,p]
    (
        ["2b00", "2b01", "2b10", "2b11"],
        ["4b1100", "4b1010"],
        ["4b0000", "4b1100", "4b1010", "4b1110"],
    ),
]


def test_matmul():
    for a, b, y in VECMUL_VALS:
        assert matmul(a, b) == bits(y)
        assert bits(a) @ b == bits(y)
        assert a @ bits(b) == bits(y)

    for a, b, y in MATMUL_VALS:
        assert bits(a) @ bits(b) == bits(y)

    with pytest.raises(TypeError):
        _ = bits("2b00") @ bits("3b000")

    with pytest.raises(TypeError):
        _ = bits("2b00") @ bits(["2b00", "2b00", "2b00"])

    with pytest.raises(TypeError):
        _ = bits(["2b00", "2b00"]) @ bits("3b000")

    with pytest.raises(TypeError):
        _ = bits(["2b00", "2b00"]) @ bits(["2b00", "2b00", "2b00"])

    with pytest.raises(TypeError):
        a = bits([["2b00", "2b00"], ["2b00", "2b00"]])
        b = bits([["2b00", "2b00"], ["2b00", "2b00"]])
        _ = a @ b
