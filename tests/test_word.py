"""Test bvwx predicate operators"""

import pytest

from bvwx import bits, cat, lrot, pack, rep, rrot, sxt, xt

E = bits()


def test_xt():
    assert xt("4b1010", 4) == bits("8b0000_1010")
    # Zero extension on multi-dimensional array will flatten
    assert xt(bits(["4b0000", "4b1111"]), 2) == bits("10b00_1111_0000")

    x = bits("4b1010")
    with pytest.raises(ValueError):
        xt(x, -1)
    assert xt(x, 0) is x
    assert xt(x, 4) == bits("8b0000_1010")

    # X Prop
    assert xt(x, "1b-") == bits("4b----")
    assert xt(x, "1bX") == bits("4bXXXX")


def test_sxt():
    assert sxt("4b1010", 4) == bits("8b1111_1010")
    assert sxt("4b0101", 4) == bits("8b0000_0101")
    # Sign extension of multi-dimensional array will flatten
    assert sxt(bits(["4b0000", "4b1111"]), 2) == bits("10b11_1111_0000")

    x1 = bits("4b1010")
    x2 = bits("4b0101")
    with pytest.raises(ValueError):
        sxt(x1, -1)
    assert sxt(x1, 0) is x1
    assert sxt(x1, 4) == bits("8b1111_1010")
    assert sxt(x2, 0) is x2
    assert sxt(x2, 4) == bits("8b0000_0101")

    # X Prop
    assert sxt(x1, "1b-") == bits("4b----")
    assert sxt(x1, "1bX") == bits("4bXXXX")


def test_lrot():
    v = bits("4b-10X")
    assert lrot(v, 0) is v
    assert str(lrot(v, 1)) == "4b10X-"
    assert str(lrot(v, 2)) == "4b0X-1"
    assert str(lrot(v, "2b10")) == "4b0X-1"
    assert str(lrot(v, "2b1-")) == "4b----"
    assert str(lrot(v, "2b1X")) == "4bXXXX"
    assert str(lrot(v, 3)) == "4bX-10"

    with pytest.raises(ValueError):
        str(lrot(v, 4))


def test_rrot():
    v = bits("4b-10X")
    assert rrot(v, 0) is v
    assert str(rrot(v, 1)) == "4bX-10"
    assert str(rrot(v, 2)) == "4b0X-1"
    assert str(rrot(v, "2b10")) == "4b0X-1"
    assert str(rrot(v, "2b1-")) == "4b----"
    assert str(rrot(v, "2b1X")) == "4bXXXX"
    assert str(rrot(v, 3)) == "4b10X-"

    with pytest.raises(ValueError):
        str(rrot(v, 4))


def test_cat():
    v = bits("4b-10X")
    assert cat() == E
    assert cat(v) == v
    assert cat("2b0X", "2b-1") == "4b-10X"
    assert cat(bits("2b0X"), bits("2b-1")) == "4b-10X"
    assert cat(0, 1) == "2b10"

    with pytest.raises(TypeError):
        _ = cat(v, 42)


def test_rep():
    assert rep(E, 4) == E
    assert rep(bits("4b-10X"), 2) == "8b-10X_-10X"


def test_pack():
    assert pack(E) is E
    assert pack("4b-10X") == "4bX01-"
    assert pack("4bX01-") == "4b-10X"
    assert pack("4b-10X", 1) == "4bX01-"
    assert pack("4b-10X", 2) == "4b0X-1"
    assert pack("32hdead_beef", 4) == "32hfeeb_daed"
    assert pack("32hfeeb_daed", 4) == "32hdead_beef"

    # Invalid values of n
    with pytest.raises(ValueError):
        pack("4b-10X", -1)
    with pytest.raises(ValueError):
        pack("4b-10X", 0)
    # x.size not divisible by n
    with pytest.raises(ValueError):
        pack("4b-10X", 3)
