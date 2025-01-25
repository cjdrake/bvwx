"""Test bvwx unary reduction operators"""

from bvwx import bits, uand, uor, uxnor, uxor

F = bits(False)
T = bits(True)
W = bits("1b-")
X = bits("1bX")


UOR = {
    "2bXX": X,
    "2bX0": X,
    "2b0X": X,
    "2bX1": X,
    "2b1X": X,
    "2bX-": X,
    "2b-X": X,
    "2b0-": W,
    "2b-0": W,
    "2b1-": T,
    "2b-1": T,
    "2b--": W,
    "2b00": F,
    "2b01": T,
    "2b10": T,
    "2b11": T,
}


def test_uor():
    for x, y in UOR.items():
        assert uor(x) == y


UAND = {
    "2bXX": X,
    "2bX0": X,
    "2b0X": X,
    "2bX1": X,
    "2b1X": X,
    "2bX-": X,
    "2b-X": X,
    "2b0-": F,
    "2b-0": F,
    "2b1-": W,
    "2b-1": W,
    "2b--": W,
    "2b00": F,
    "2b01": F,
    "2b10": F,
    "2b11": T,
}


def test_uand():
    for x, y in UAND.items():
        assert uand(x) == y


UXNOR = {
    "2bXX": X,
    "2bX0": X,
    "2b0X": X,
    "2bX1": X,
    "2b1X": X,
    "2bX-": X,
    "2b-X": X,
    "2b0-": W,
    "2b-0": W,
    "2b1-": W,
    "2b-1": W,
    "2b--": W,
    "2b00": T,
    "2b01": F,
    "2b10": F,
    "2b11": T,
}


def test_uxnor():
    for x, y in UXNOR.items():
        assert uxnor(x) == y


UXOR = {
    "2bXX": X,
    "2bX0": X,
    "2b0X": X,
    "2bX1": X,
    "2b1X": X,
    "2bX-": X,
    "2b-X": X,
    "2b0-": W,
    "2b-0": W,
    "2b1-": W,
    "2b-1": W,
    "2b--": W,
    "2b00": F,
    "2b01": T,
    "2b10": T,
    "2b11": F,
}


def test_uxor():
    for x, y in UXOR.items():
        assert uxor(x) == y
