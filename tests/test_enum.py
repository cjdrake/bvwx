"""Test bvwx Enum"""

# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false
# pyright: reportOperatorIssue=false

import pytest

from bvwx import Enum, Vec


class Color(Enum):
    """Boilerplate bit array enum."""

    RED = "2b00"
    GREEN = "2b01"
    BLUE = "2b10"


def test_empty():
    # Empty Enum is not supported
    with pytest.raises(ValueError):

        class EmptyEnum(Enum):
            pass


def test_basic():
    assert len(Color.RED) == 2
    assert repr(Color.RED) == "Color.RED"
    assert str(Color.RED) == "Color.RED"
    assert Color.RED.name == "RED"
    assert Color.RED.data[1] == 0b00
    assert str(Color.RED) == "Color.RED"
    assert Color("2b00") is Color.RED
    assert Color(Vec[2](0b11, 0b00)) is Color.RED

    assert len(Color.X) == 2
    assert repr(Color.X) == "Color.X"
    assert str(Color.X) == "Color.X"
    assert Color.X.name == "X"
    assert Color.X.data == (0b00, 0b00)
    assert str(Color.X) == "Color.X"
    assert Color("2bXX") is Color.X
    assert Color.xes() is Color.X
    assert Color(Vec[2](0, 0)) is Color.X

    assert len(Color.DC) == 2
    assert repr(Color.DC) == "Color.DC"
    assert str(Color.DC) == "Color.DC"
    assert Color.DC.name == "DC"
    assert Color.DC.data == (0b11, 0b11)
    assert str(Color.DC) == "Color.DC"
    assert Color("2b--") is Color.DC
    assert Color.dcs() is Color.DC
    assert Color(Vec[2](0b11, 0b11)) is Color.DC

    assert str(Color("2b11").name) == "Color(2b11)"
    assert str(Color(Vec[2](0b00, 0b11)).name) == "Color(2b11)"
    assert repr(Color("2b11")) == 'Color("2b11")'
    assert str(Color("2b11")) == "Color(2b11)"

    assert Color.BLUE.vcd_var() == "string"


def test_typing():
    """Advanced type behavior."""
    assert ~Color.GREEN is Color.BLUE
    assert ~Color.BLUE is Color.GREEN

    assert isinstance(~Color.RED, Color)
    assert (~Color.RED).name == "Color(2b11)"

    assert (Color.GREEN << 1) is Color.BLUE
    assert (Color.BLUE >> 1) is Color.GREEN


def test_slicing():
    assert Color.GREEN[0] == "1b1"
    assert Color.GREEN[1] == "1b0"


def test_enum_error():
    """Test enum spec errors."""
    with pytest.raises(ValueError):

        class InvalidName(Enum):
            X = "4bXXXX"

        _ = InvalidName()

    with pytest.raises(ValueError):

        class InvalidData(Enum):
            FOO = "4bXXXX"

        _ = InvalidData()

    # The literal must be a str
    with pytest.raises(TypeError):

        class InvalidType(Enum):
            FOO = 42

        _ = InvalidType()

    with pytest.raises(ValueError):

        class InvalidMembers(Enum):
            A = "2b00"
            B = "3b000"

        _ = InvalidMembers()

    with pytest.raises(ValueError):

        class DuplicateMembers(Enum):
            A = "2b00"
            B = "2b01"
            C = "2b00"
