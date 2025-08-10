"""Test Bits methods."""

# pyright: reportArgumentType=false
# pyright: reportCallIssue=false

import pytest

from bvwx import Array, Empty, Enum, Scalar, Struct, Union, Vec, bits, u2bv

E = bits()
F = bits(False)
T = bits(True)
W = bits("1b-")
X = bits("1bX")


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
    assert Vec[4].xprop(bits("1b-")) == "4b----"


def test_type_resolution():
    class Color(Enum):
        RED = "2b00"
        GREEN = "2b01"
        BLUE = "2b10"

    # Downgrade Enum to Vec
    y = bits("2b00") | Color.RED
    assert type(y) is Vec[2]

    # Downgrade Array to Vec
    y = Array[4, 4].rand() | Vec[16].rand()
    assert type(y) is Vec[16]


def test_type_cast():
    x1 = bits("4b1001")
    x2 = bits(["2b01", "2b10"])

    x3 = Vec[4].cast(x2)
    assert type(x3) is Vec[4]
    assert x3 == x1

    with pytest.raises(TypeError):
        Vec[3].cast(x1)


def test_bool():
    assert not bool(E)
    assert not bool(F)
    assert bool(T)
    assert not bool(bits("4b0000"))
    assert bool(bits("4b0001"))
    assert bool(bits("4b0010"))
    assert bool(bits("4b0100"))
    assert bool(bits("4b1000"))

    with pytest.raises(ValueError):
        _ = bool(W)
    with pytest.raises(ValueError):
        _ = bool(X)
    with pytest.raises(ValueError):
        _ = bool(bits("3b10X"))
    with pytest.raises(ValueError):
        _ = bool(bits("3b10-"))


def test_hash():
    s: set[Vec] = set()
    s.add(u2bv(0))
    s.add(u2bv(1))
    s.add(u2bv(2))
    s.add(u2bv(3))
    s.add(u2bv(2))
    s.add(u2bv(1))
    s.add(u2bv(0))
    assert len(s) == 4


class MyStruct(Struct):
    a: Vec[8]
    b: Vec[8]


class MyUnion(Union):
    a: Vec[4]
    b: Vec[8]


def test_bug_3():
    s: set[MyStruct] = set()
    s.add(MyStruct(a="8h00"))
    s.add(MyStruct(a="8h11"))
    s.add(MyStruct(a="8h22"))
    s.add(MyStruct(a="8h33"))
    s.add(MyStruct(a="8h22"))
    s.add(MyStruct(a="8h11"))
    s.add(MyStruct(a="8h00"))
    assert len(s) == 4

    s.clear()
    s.add(MyUnion("4b0001"))
    s.add(MyUnion("4b0010"))
    s.add(MyUnion("4b0100"))
    s.add(MyUnion("4b1000"))
    s.add(MyUnion("4b0100"))
    s.add(MyUnion("4b0010"))
    s.add(MyUnion("4b0001"))
    assert len(s) == 4


X0 = bits([])
X1 = bits("1b0")
X2 = bits("4b-10X")
X3 = bits(["4b-10X", "4b-10X"])

X4 = bits([["4b-10X", "4b-10X"], ["4b-10X", "4b-10X"]])

X4_REPR = """\
bits([["4b-10X", "4b-10X"],
      ["4b-10X", "4b-10X"]])"""

X4_STR = """\
[[4b-10X, 4b-10X],
 [4b-10X, 4b-10X]]"""

X5 = bits(
    [
        [["4b-10X", "4b-10X"], ["4b-10X", "4b-10X"]],
        [["4b-10X", "4b-10X"], ["4b-10X", "4b-10X"]],
    ]
)

X5_REPR = """\
bits([[["4b-10X", "4b-10X"],
       ["4b-10X", "4b-10X"]],

      [["4b-10X", "4b-10X"],
       ["4b-10X", "4b-10X"]]])"""

X5_STR = """\
[[[4b-10X, 4b-10X],
  [4b-10X, 4b-10X]],

 [[4b-10X, 4b-10X],
  [4b-10X, 4b-10X]]]"""


def test_repr():
    assert repr(X0) == "bits([])"
    assert repr(X1) == 'bits("1b0")'
    assert repr(X2) == 'bits("4b-10X")'
    assert repr(X3) == 'bits(["4b-10X", "4b-10X"])'
    assert repr(X4) == X4_REPR
    assert repr(X5) == X5_REPR


def test_str():
    assert str(X0) == "[]"
    assert str(X1) == "1b0"
    assert str(X2) == "4b-10X"
    assert str(X3) == "[4b-10X, 4b-10X]"
    assert str(X4) == X4_STR
    assert str(X5) == X5_STR


def test_vec_getitem():
    assert X1[0] == "1b0"

    assert X2[3] == "1b-"
    assert X2[2] == "1b1"
    assert X2[1] == "1b0"
    assert X2[0] == "1bX"

    assert X2["2b11"] == "1b-"
    assert X2["2b10"] == "1b1"
    assert X2["2b01"] == "1b0"
    assert X2["2b00"] == "1bX"

    assert X2[bits("2b11")] == "1b-"
    assert X2[bits("2b10")] == "1b1"
    assert X2[bits("2b01")] == "1b0"
    assert X2[bits("2b00")] == "1bX"

    assert X2[-1] == "1b-"
    assert X2[-2] == "1b1"
    assert X2[-3] == "1b0"
    assert X2[-4] == "1bX"

    assert X2[0:1] == "1bX"
    assert X2[0:2] == "2b0X"
    assert X2[0:3] == "3b10X"
    assert X2[0:4] == "4b-10X"

    assert X2[:-3] == "1bX"
    assert X2[:-2] == "2b0X"
    assert X2[:-1] == "3b10X"

    assert X2[1:2] == "1b0"
    assert X2[1:3] == "2b10"
    assert X2[1:4] == "3b-10"

    assert X2[-3:2] == "1b0"
    assert X2[-3:3] == "2b10"
    assert X2[-3:4] == "3b-10"

    assert X2[2:3] == "1b1"
    assert X2[2:4] == "2b-1"

    assert X2[3:4] == "1b-"

    # Invalid index
    with pytest.raises(IndexError):
        _ = X2[4]
    # Slice step not supported
    with pytest.raises(ValueError):
        _ = X2[0:4:1]


def test_array_class_getitem():
    assert Array[0] is Empty
    assert Array[1] is Scalar
    assert Array[2] is Vec[2]
    assert Array[2, 2].shape == (2, 2)
    with pytest.raises(ValueError):
        _ = Array[-1]
    with pytest.raises(ValueError):
        _ = Array[2, 2, 1]
    with pytest.raises(ValueError):
        _ = Array[2, 2, 0]
    with pytest.raises(ValueError):
        _ = Array[2, 2, -1]
    with pytest.raises(TypeError):
        _ = Array["invalid"]


def test_vec_class_getitem():
    assert Vec[0] is Empty
    assert Vec[1] is Scalar
    assert Vec[2].shape == (2,)
    with pytest.raises(ValueError):
        _ = Vec[-1]
    with pytest.raises(TypeError):
        _ = Vec["invalid"]


def test_vec_iter():
    x = bits("4b-10X")
    assert list(x) == ["1bX", "1b0", "1b1", "1b-"]
    assert list(reversed(x)) == ["1b-", "1b1", "1b0", "1bX"]


def test_scalar_iter():
    x = bits("1b0")
    assert list(x) == ["1b0"]
    assert list(reversed(x)) == ["1b0"]


def test_empty():
    assert not list(E)
    assert list(reversed(E)) == [E]
    with pytest.raises(IndexError):
        E[0]


def test_slicing():
    """Test bits slicing behavior."""
    x = bits(
        [
            ["4b0000", "4b0001", "4b0010", "4b0011"],
            ["4b0100", "4b0101", "4b0110", "4b0111"],
            ["4b1000", "4b1001", "4b1010", "4b1011"],
            ["4b1100", "4b1101", "4b1110", "4b1111"],
        ]
    )

    assert x.shape == (4, 4, 4)

    with pytest.raises(IndexError):
        x[-5]
    with pytest.raises(ValueError):
        x["invalid"]
    # Slice step not supported
    with pytest.raises(ValueError):
        x[0:4:1]
    # Invalid dimension
    with pytest.raises(ValueError):
        x[0, 0, 0, 0]
    # Invalid slice type
    with pytest.raises(TypeError):
        x[42.0]

    assert x == x[:]
    assert x == x[0:4]
    assert x == x[-4:]
    assert x == x[-5:]
    assert x == x[:, :]
    assert x == x[:, :, :]

    assert x[0] == x[0, :]
    assert x[0] == x[0, 0:4]
    assert x[0] == x[0, -4:]
    assert x[0] == x[0, -5:]
    assert x[0] == x[0, :, :]

    assert x[0] == bits(["4b0000", "4b0001", "4b0010", "4b0011"])
    assert x[1] == bits(["4b0100", "4b0101", "4b0110", "4b0111"])
    assert x[2] == bits(["4b1000", "4b1001", "4b1010", "4b1011"])
    assert x[3] == bits(["4b1100", "4b1101", "4b1110", "4b1111"])

    assert x[0, 0] == x[0, 0, :]
    assert x[0, 0] == x[0, 0, 0:4]
    assert x[0, 0] == x[0, 0, -4:]
    assert x[0, 0] == x[0, 0, -5:]

    assert x[0, 0] == bits("4b0000")
    assert x[1, 1] == bits("4b0101")
    assert x[2, 2] == bits("4b1010")
    assert x[3, 3] == bits("4b1111")

    assert x[0, :, 0] == bits("4b1010")
    assert x[1, :, 1] == bits("4b1100")
    assert x[2, :, 2] == bits("4b0000")
    assert x[3, :, 3] == bits("4b1111")

    assert x[0, 0, :-1] == bits("3b000")
    assert x[0, 0, :-2] == bits("2b00")
    assert x[0, 0, :-3] == bits("1b0")
    assert x[0, 0, :-4] == bits()

    assert x[0, 0, 0] == F
    assert x["1b0", "1b0", "1b0"] == F
    assert x[F, F, F] == F
    assert x[-4, -4, -4] == F
    assert x[3, 3, 3] == T
    assert x[-1, -1, -1] == T


def test_array_reshape():
    a = Array[2, 3, 4]
    v = Vec[24]
    x = a(0, 0)
    assert x.shape == (2, 3, 4)
    assert x.size == 24

    y = x.reshape((2, 3, 4))
    assert type(y) is a
    assert y == x

    y = x.reshape((4, 3, 2))
    assert type(y) is Array[4, 3, 2]
    assert y == x

    y = x.reshape((24,))
    assert type(y) is v
    assert y == x

    y = x.flatten()
    assert type(y) is v
    assert y == x

    with pytest.raises(ValueError):
        x.reshape((4, 4, 4))


def test_vec_reshape():
    v = Vec[24]
    x = v(0, 0)
    assert x.shape == (24,)
    assert x.size == 24

    y = x.reshape((2, 3, 4))
    assert type(y) is Array[2, 3, 4]
    assert y == x

    y = x.reshape((24,))
    assert type(y) is v
    assert y == x

    y = x.flatten()
    assert type(y) is v
    assert y == x

    with pytest.raises(ValueError):
        x.reshape((4, 4, 4))


def test_vcd():
    assert bits("4b-10X").vcd_var() == "logic"
    assert bits("4b-10X").vcd_val() == "x10x"


def test_count():
    x = bits("8b-10X_-10X")
    assert x.count_xes() == 2
    assert x.count_zeros() == 2
    assert x.count_ones() == 2
    assert x.count_dcs() == 2
    assert x.count_unknown() == 4

    assert not bits("4b0000").onehot()
    assert bits("4b1000").onehot()
    assert bits("4b0001").onehot()
    assert not bits("4b1001").onehot()
    assert not bits("4b1101").onehot()

    assert bits("4b0000").onehot0()
    assert bits("4b1000").onehot0()
    assert not bits("4b1010").onehot0()
    assert not bits("4b1011").onehot0()

    assert not bits("4b1111").has_0
    assert bits("4b1110").has_0
    assert not bits("4b0000").has_1
    assert bits("4b0001").has_1

    assert not bits("4b0000").has_x
    assert bits("4b00X0").has_x
    assert not bits("4b0000").has_dc
    assert bits("4b00-0").has_dc
    assert not bits("4b0000").has_unknown
    assert bits("4b00X0").has_unknown
    assert bits("4b00-0").has_unknown
