"""Bits Data Types

A bit is a 4-state logical value in the set {``0``, ``1``, ``X``, ``W``}:

    * 0 is Boolean zero or "False"
    * 1 is Boolean one or "True"
    * X is an uninitialized or metastable value
    * W is a "don't care" value

The values ``0`` and ``1`` are "known".
The values ``X`` and ``W`` are "unknown".

Children::

                  Array
                    |
                  Vector
                    |
      +-------+-----+------+------+
      |       |     |      |      |
    Scalar  Empty  Enum  Struct Union

Do **NOT** construct an Array object directly.
Use one of the factory functions:

    * bits
    * stack
    * lit2bv
    * u2bv
    * i2bv
"""

from __future__ import annotations

import math
import random
from collections.abc import Iterator
from functools import partial
from types import GenericAlias
from typing import Any, Self

from . import _lbool as lb
from ._lbool import lbv
from ._util import clog2, mask

_ArrayShape: dict[tuple[int, ...], type[Array]] = {}


def _b2s(arg: int) -> Array:
    try:
        return bool2scalar[arg]
    except IndexError as e:
        s = f"Expected arg: int in {{0, 1}}, got {arg}"
        raise ValueError(s) from e


def _i2v(arg: int, size: int) -> Array:
    if arg < 0:
        return i2bv(arg, size)
    return u2bv(arg, size)


def _expect_size[T: Array](arg: T, size: int) -> T:
    if arg.size != size:
        raise TypeError(f"Expected size {size}, got {arg.size}")
    return arg


def expect_array(arg: ArrayLike) -> Array:
    """Any Array-like object that defines its own size"""
    # arg: Array | str | int
    if isinstance(arg, int):
        return _b2s(arg)
    # arg: Array | str
    if isinstance(arg, str):
        return lit2bv(arg)
    # arg: Array
    return arg


def expect_uint(arg: UintLike) -> Array:
    """Any Array-like object that defines its own size"""
    # arg: Array | str | int
    if isinstance(arg, int):
        return u2bv(arg)
    # arg: Array | str
    if isinstance(arg, str):
        return lit2bv(arg)
    # arg: Array
    return arg


def expect_array_size(arg: ArrayLike, size: int) -> Array:
    """Any Array-Like object that may or may not define its own size"""
    # arg: Array | str | int
    if isinstance(arg, int):
        return _i2v(arg, size)
    # arg: Array | str
    if isinstance(arg, str):
        x = lit2bv(arg)
        return _expect_size(x, size)
    # arg: Array
    return _expect_size(arg, size)


def expect_vec_size(arg: VectorLike, size: int) -> Array:
    """Any Vector-Like object that may or may not define its own size"""
    # arg: Vector | str | int
    if isinstance(arg, int):
        return _i2v(arg, size)
    # arg: Vector | str
    if isinstance(arg, str):
        x = lit2bv(arg)
        return _expect_size(x, size)
    # arg: Vector
    if len(arg.shape) != 1:
        s = f"Expected one-dimensional shape, got {arg.shape}"
        raise TypeError(s)
    return _expect_size(arg, size)


def expect_scalar(arg: ScalarLike) -> Array:
    """Any Scalar-like object"""
    # arg: Scalar | str | int
    if isinstance(arg, int):
        return _b2s(arg)
    # arg: Scalar | str
    if isinstance(arg, str):
        x = lit2bv(arg)
        return _expect_size(x, 1)
    # arg: Scalar
    return _expect_size(arg, 1)


def resolve_type[T: Array](x0: T, x1: Array) -> type[T] | type[Array]:
    t = type(x0)

    # T (op) T -> T
    if t is type(x1):
        return t

    # Otherwise, downgrade to Vector
    return vec_cls(x0.size)


class ArrayGenericAlias(GenericAlias):
    def __repr__(self) -> str:
        return self.__origin__.__name__

    def __str__(self) -> str:
        return self.__origin__.__name__


class Array[*Shape]:
    """Multi dimensional array of bits.

    To create an ``Array`` instance, use the ``bits`` function:

    >>> x = bits(["4b0100", "4b1110"])

    ``Array`` implements ``size`` and ``shape`` attributes,
    and the ``__getitem__`` method.
    ``Array`` does **NOT** implement a ``__len__`` method.

    >>> x.size
    8
    >>> x.shape
    (2, 4)
    >>> x[0]
    bits("4b0100")
    >>> x[1]
    bits("4b1110")
    >>> x[0,0]
    bits("1b0")

    An ``Array`` may be converted into an equal-size, multi-dimensional ``Array``
    using the ``reshape`` method:

    >>> x.reshape((4,2))
    bits(["2b00", "2b01", "2b10", "2b11"])

    An ``Array`` may be converted into an equal-size, one-dimensional ``Vector``
    using the ``flatten`` method:

    >>> x.flatten()
    bits("8b1110_0100")
    """

    __slots__ = ("_data",)

    shape: tuple[int, ...]
    size: int
    _dmax: int

    def __class_getitem__(cls, key: int | tuple[int, ...]) -> ArrayGenericAlias:
        if isinstance(key, int):
            size: int = key
            if size < 0:
                raise ValueError(f"Expected size ≥ 0, got {size}")
            return ArrayGenericAlias(vec_cls(size), (size,))

        shape: tuple[int, ...] = key
        for i, n in enumerate(shape):
            if n <= 1:
                s = f"For shape dimension {i}: expected n > 1, got {n}"
                raise ValueError(s)
        return ArrayGenericAlias(array_cls(shape), shape)

    @classmethod
    def _cast_data(cls, d0: int, d1: int) -> Self:
        return cast_data(cls, d0, d1)

    @classmethod
    def xs(cls) -> Self:
        """Return an instance filled with ``X`` bits.

        For example:

        >>> Array[4].xs()
        bits("4bXXXX")
        """
        return cls._cast_data(0, 0)

    @classmethod
    def zeros(cls) -> Self:
        """Return an instance filled with ``0`` bits.

        For example:

        >>> Array[4].zeros()
        bits("4b0000")
        """
        return cls._cast_data(cls._dmax, 0)

    @classmethod
    def ones(cls) -> Self:
        """Return an instance filled with ``1`` bits.

        For example:

        >>> Array[4].ones()
        bits("4b1111")
        """
        return cls._cast_data(0, cls._dmax)

    @classmethod
    def ws(cls) -> Self:
        """Return an instance filled with ``-`` bits.

        For example:

        >>> Array[4].ws()
        bits("4b----")
        """
        return cls._cast_data(cls._dmax, cls._dmax)

    @classmethod
    def rand(cls) -> Self:
        """Return an instance filled with random bits."""
        d1 = random.getrandbits(cls.size)
        d0 = cls._dmax ^ d1
        return cls._cast_data(d0, d1)

    @classmethod
    def xprop(cls, sel: Array) -> Self:
        """Propagate ``X`` in a wildcard pattern (default case).

        If ``sel`` contains an ``X``, propagate ``X``.
        Otherwise, treat as a "don't care", and propagate ``-``.

        For example:

        >>> def f(x: Array[1]) -> Array[1]:
        ...     match x:
        ...         case "1b0":
        ...             return bits("1b1")
        ...         case _:
        ...             return Array[1].xprop(x)

        >>> f(bits("1b0"))  # Match!
        bits("1b1")
        >>> f(bits("1b1"))  # No match; No X prop
        bits("1b-")
        >>> f(bits("1bX"))  # No match; Yes X prop
        bits("1bX")

        Args:
            sel: Array object, typically a ``match`` subject

        Returns:
            Class instance filled with either ``-`` or ``X``.
        """
        if sel.has_x():
            return cls.xs()
        return cls.ws()

    @classmethod
    def _norm_key(cls, keys: list[Key]) -> tuple[tuple[int, int], ...]:
        ndim = len(cls.shape)
        klen = len(keys)

        if klen > ndim:
            s = f"Expected ≤ {ndim} key items, got {klen}"
            raise ValueError(s)

        # Append ':' to the end
        for _ in range(ndim - klen):
            keys.append(slice(None))

        # Normalize key dimensions
        def f(n: int, key: Key) -> tuple[int, int]:
            if isinstance(key, int):
                i = _norm_index(n, key)
                return (i, i + 1)
            # slice | Array | str
            if isinstance(key, slice):
                return _norm_slice(n, key)
            # Array | str
            if isinstance(key, str):
                key = lit2bv(key)
            i = _norm_index(n, key.to_uint())
            return (i, i + 1)

        return tuple(f(n, key) for n, key in zip(cls.shape, keys))

    def __init__(self, d0: int, d1: int) -> None:
        assert d0 <= self._dmax and d1 <= self._dmax
        self._data = (d0, d1)

    def __hash__(self) -> int:
        return hash((self.size,) + self._data)

    def __eq__(self, obj: Any) -> bool:
        if isinstance(obj, str):
            size, data = lb.parse_lit(obj)
            return size == self.size and data == self._data
        if isinstance(obj, Array):
            return obj.size == self.size and obj._data == self._data
        return False

    def _str(self) -> str:
        prefix = f"{self.size}b"
        chars = [lb.to_char[self._get_index(0)]]
        for i in range(1, self.size):
            if i % 4 == 0:
                chars.append("_")
            chars.append(lb.to_char[self._get_index(i)])
        return prefix + "".join(reversed(chars))

    def _get_index(self, i: int) -> lbv:
        d0 = (self._data[0] >> i) & 1
        d1 = (self._data[1] >> i) & 1
        return d0, d1

    def _get_slice(self, i: int, j: int) -> tuple[int, lbv]:
        size = j - i
        m = mask(size)
        d0 = (self._data[0] >> i) & m
        d1 = (self._data[1] >> i) & m
        return size, (d0, d1)

    def __len__(self) -> int:
        return self.shape[0]

    def __getitem__(self, key: Key | tuple[Key, ...]) -> Array:
        if isinstance(key, (int, slice, Array, str)):
            keys = [key]
        else:
            keys = list(key)
        return _sel(self, self._norm_key(keys))

    def __iter__(self) -> Iterator[Array]:
        for i in range(self.shape[0]):
            yield _sel(x=self, key=self._norm_key([i]))

    def reshape(self, shape: tuple[int, ...]) -> Array:
        if shape == self.shape:
            return self
        if math.prod(shape) != self.size:
            s = f"Expected shape with size {self.size}, got {shape}"
            raise ValueError(s)
        if len(shape) == 1:
            return vec_obj(size=shape[0], d0=self._data[0], d1=self._data[1])
        return array_obj(shape, d0=self._data[0], d1=self._data[1])

    def flatten(self) -> Array:
        raise NotImplementedError()  # pragma: no cover

    def __bool__(self) -> bool:
        """Convert to Python ``bool``.

        An ``Array`` object is ``True`` if its value is known nonzero.

        For example:

        >>> bool(bits("1b0"))
        False
        >>> bool(bits("1b1"))
        True
        >>> bool(bits("4b0000"))
        False
        >>> bool(bits("4b1010"))
        True

        .. warning::
            Be cautious about using any expression that *might* have an unknown
            value as the condition of a Python ``if`` or ``while`` statement.

        Raises:
            ValueError: Contains any unknown bits.
        """
        return self.to_uint() != 0

    def __int__(self) -> int:
        """Convert to Python ``int``.

        Use two's complement representation:

        * If most significant bit is ``1``, result will be negative.
        * If most significant bit is ``0``, result will be non-negative.

        For example:

        >>> int(bits("4b1010"))
        -6
        >>> int(bits("4b0101"))
        5

        Raises:
            ValueError: Contains any unknown bits.
        """
        return self.to_int()

    def to_uint(self) -> int:
        """Convert to unsigned integer.

        Returns:
            A non-negative ``int``.

        Raises:
            ValueError: Contains any unknown bits.
        """
        if self.has_xw():
            raise ValueError("Cannot convert unknown to uint")
        return self._data[1]

    def to_int(self) -> int:
        """Convert to signed integer.

        Returns:
            An ``int``, from two's complement encoding.

        Raises:
            ValueError: Contains any unknown bits.
        """
        if self.has_xw():
            raise ValueError("Cannot convert unknown to int")
        if self.size == 0:
            return 0
        sign = self._get_index(self.size - 1)
        if sign == lb.T:
            return -(self._data[0] + 1)
        return self._data[1]

    # Bitwise Operations
    def __invert__(self) -> Self:
        return bits_not(self)

    def __or__(self, other: ArrayLike) -> Self | Array:
        other = expect_array_size(other, self.size)
        return bits_or(self, other)

    def __ror__(self, other: ArrayLike) -> Array:
        other = expect_array_size(other, self.size)
        return bits_or(other, self)

    def __and__(self, other: ArrayLike) -> Self | Array:
        other = expect_array_size(other, self.size)
        return bits_and(self, other)

    def __rand__(self, other: ArrayLike) -> Array:
        other = expect_array_size(other, self.size)
        return bits_and(other, self)

    def __xor__(self, other: ArrayLike) -> Self | Array:
        other = expect_array_size(other, self.size)
        return bits_xor(self, other)

    def __rxor__(self, other: ArrayLike) -> Array:
        other = expect_array_size(other, self.size)
        return bits_xor(other, self)

    # Note: Drop carry-out
    def __lshift__(self, n: UintLike) -> Self:
        n = expect_uint(n)
        return bits_lsh(self, n)

    def __rlshift__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_lsh(other, self)

    # Note: Drop carry-out
    def __rshift__(self, n: UintLike) -> Self:
        n = expect_uint(n)
        return bits_rsh(self, n)

    def __rrshift__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_rsh(other, self)

    # Note: Keep carry-out
    def __add__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        s, co = bits_add(self, other, scalar0)
        return bits_cat(s, co)

    def __radd__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        s, co = bits_add(other, self, scalar0)
        return bits_cat(s, co)

    # Note: Keep carry-out
    def __sub__(self, other: ArrayLike) -> Array:
        other = expect_array_size(other, self.size)
        s, co = bits_sub(self, other)
        return bits_cat(s, co)

    def __rsub__(self, other: ArrayLike) -> Array:
        other = expect_array_size(other, self.size)
        s, co = bits_sub(other, self)
        return bits_cat(s, co)

    # Note: Keep carry-out
    def __neg__(self) -> Array:
        s, co = bits_neg(self)
        return bits_cat(s, co)

    def __mul__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_mul(self, other)

    def __rmul__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_mul(other, self)

    def __floordiv__(self, other: ArrayLike) -> Self:
        other = expect_array(other)
        return bits_div(self, other)

    def __rfloordiv__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_div(other, self)

    def __mod__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_mod(self, other)

    # Note: __rmod__ does not work b/c str implements % operator

    def __matmul__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_matmul(self, other)

    def __rmatmul__(self, other: ArrayLike) -> Array:
        other = expect_array(other)
        return bits_matmul(other, self)

    def count_zeros(self) -> int:
        """Return count of of ``0`` bits."""
        d: int = self._data[0] & (self._data[1] ^ self._dmax)
        return d.bit_count()

    def count_ones(self) -> int:
        """Return count of ``1`` bits."""
        d: int = (self._data[0] ^ self._dmax) & self._data[1]
        return d.bit_count()

    def count_xs(self) -> int:
        """Return count of ``X`` bits."""
        d: int = (self._data[0] | self._data[1]) ^ self._dmax
        return d.bit_count()

    def count_ws(self) -> int:
        """Return count of ``-`` bits."""
        d: int = self._data[0] & self._data[1]
        return d.bit_count()

    def count_unknown(self) -> int:
        """Return count of unknown bits."""
        d: int = self._data[0] ^ self._data[1] ^ self._dmax
        return d.bit_count()

    def onehot(self) -> bool:
        """Return True if contains exactly one ``1`` bit."""
        return not self.has_xw() and self.count_ones() == 1

    def onehot0(self) -> bool:
        """Return True if contains at most one ``1`` bit."""
        return not self.has_xw() and self.count_ones() <= 1

    def has_0(self) -> bool:
        """Return True if contains at least one ``0`` bit."""
        return bool(self._data[0] & (self._data[1] ^ self._dmax))

    def has_1(self) -> bool:
        """Return True if contains at least one ``1`` bit."""
        return bool((self._data[0] ^ self._dmax) & self._data[1])

    def has_x(self) -> bool:
        """Return True if contains at least one ``X`` bit."""
        return bool((self._data[0] | self._data[1]) ^ self._dmax)

    def has_w(self) -> bool:
        """Return True if contains at least one ``-`` bit."""
        return bool(self._data[0] & self._data[1])

    def has_xw(self) -> bool:
        """Return True if contains at least one unknown bit."""
        return bool(self._data[0] ^ self._data[1] ^ self._dmax)

    def has_unknown(self) -> bool:
        """Return True if contains at least one unknown bit."""
        return bool(self._data[0] ^ self._data[1] ^ self._dmax)

    def vcd_var(self) -> str:
        """Return VCD variable type."""
        return "logic"

    def vcd_val(self) -> str:
        """Return VCD variable value."""
        return "".join(lb.to_vcd_char[self._get_index(i)] for i in range(self.size - 1, -1, -1))


def _empty_repr(self: Array) -> str:
    return "bits([])"


def _empty_str(self: Array) -> str:
    return "[]"


def _vec_repr(self: Array) -> str:
    return f'bits("{self._str()}")'


def _vec_str(self: Array) -> str:
    return self._str()


def _array_repr(self: Array) -> str:
    return f"bits({_repr(indent='      ', x=self)})"


def _array_str(self: Array) -> str:
    return _str(indent=" ", x=self)


def _vec_flatten(self: Array) -> Array:
    return self


def _array_flatten(self: Array) -> Array:
    return vec_obj(size=self.size, d0=self._data[0], d1=self._data[1])


def _array_new(shape: tuple[int, ...]) -> type[Array]:
    assert shape
    if shape == (0,):
        name = "Empty"
    elif shape == (1,):
        name = "Scalar"
    elif len(shape) == 1:
        name = f"Vector[{shape[0]}]"
    elif len(shape) == 2:  # noqa: PLR2004
        name = f"Matrix[{shape[0]},{shape[1]}]"
    else:
        s = ",".join(str(n) for n in shape)
        name = f"Array[{s}]"

    size = math.prod(shape)
    dmax = mask(size)
    ns: dict[str, Any] = {"__slots__": (), "shape": shape, "size": size, "_dmax": dmax}
    cls = type(name, (Array,), ns)

    if len(shape) == 1:
        if shape == (0,):
            setattr(cls, "__repr__", _empty_repr)
            setattr(cls, "__str__", _empty_str)
        else:
            setattr(cls, "__repr__", _vec_repr)
            setattr(cls, "__str__", _vec_str)
        setattr(cls, "flatten", _vec_flatten)
    else:
        setattr(cls, "__repr__", _array_repr)
        setattr(cls, "__str__", _array_str)
        setattr(cls, "flatten", _array_flatten)

    return cls


def array_cls(shape: tuple[int, ...]) -> type[Array]:
    """Return Array[shape] type."""
    assert shape
    assert len(shape) == 1 and shape[0] >= 0 or all(isinstance(n, int) and n > 1 for n in shape)

    try:
        return _ArrayShape[shape]
    except KeyError:
        cls = _array_new(shape)
        _ArrayShape[shape] = cls
        return cls


def vec_cls(size: int) -> type[Array]:
    return array_cls(shape=(size,))


def scalar_cls() -> type[Array]:
    return vec_cls(size=1)


def empty_cls() -> type[Array]:
    return vec_cls(size=0)


def array_obj(shape: tuple[int, ...], d0: int, d1: int) -> Array:
    return array_cls(shape)(d0, d1)


def vec_obj(size: int, d0: int, d1: int) -> Array:
    return vec_cls(size)(d0, d1)


_scalars: dict[lbv, Array | None] = {
    lb.X: None,
    lb.F: None,
    lb.T: None,
    lb.W: None,
}


def scalar_obj(d0: int, d1: int) -> Array:
    data = (d0, d1)
    x = _scalars[data]
    if x is None:
        x = scalar_cls()(d0, d1)
        _scalars[data] = x
    return x


scalarX = scalar_obj(*lb.X)
scalar0 = scalar_obj(*lb.F)
scalar1 = scalar_obj(*lb.T)
scalarW = scalar_obj(*lb.W)

bool2scalar = (scalar0, scalar1)


_empty: Array | None = None


def empty_obj() -> Array:
    global _empty  # noqa: PLW0603
    if _empty is None:
        _empty = empty_cls()(d0=0, d1=0)
    return _empty


def cast_data[T: Array](cls: type[T], d0: int, d1: int) -> T:
    obj: T = object.__new__(cls)
    obj._data = (d0, d1)
    return obj


def cast[T: Array](cls: type[T], x: Array) -> T:
    """Convert Array object to an instance of this class.

    For example, to cast an ``Array[2,2]`` to a ``Vector[4]``:

    >>> x = bits(["2b00", "2b11"])
    >>> cast(Array[4], x)
    bits("4b1100")

    Raises:
        TypeError: Object size does not match this class size.
    """
    if x.size != cls.size:
        raise TypeError(f"Expected size {cls.size}, got {x.size}")
    return cls._cast_data(x._data[0], x._data[1])


# Type Aliases
type ArrayLike = Array | str | int
type VectorLike = Array | str | int
type ScalarLike = Array | str | int
type UintLike = Array | str | int
type KeySlice = slice[int | None, int | None, None]
type Key = UintLike | KeySlice


# Bitwise
def bits_not[T: Array](x: T) -> T:
    d0, d1 = lb.not_(x._data)
    return x._cast_data(d0, d1)


def bits_or[T: Array](x0: T, x1: Array) -> T | Array:
    d0, d1 = lb.or_(x0._data, x1._data)
    t = resolve_type(x0, x1)
    return t._cast_data(d0, d1)


def bits_and[T: Array](x0: T, x1: Array) -> T | Array:
    d0, d1 = lb.and_(x0._data, x1._data)
    t = resolve_type(x0, x1)
    return t._cast_data(d0, d1)


def bits_xnor[T: Array](x0: T, x1: Array) -> T | Array:
    d0, d1 = lb.xnor(x0._data, x1._data)
    t = resolve_type(x0, x1)
    return t._cast_data(d0, d1)


def bits_xor[T: Array](x0: T, x1: Array) -> T | Array:
    d0, d1 = lb.xor(x0._data, x1._data)
    t = resolve_type(x0, x1)
    return t._cast_data(d0, d1)


# Unary
def bits_uor(x: Array) -> Array:
    if x.has_x():
        return scalarX
    if x.has_1():
        return scalar1
    if x.has_w():
        return scalarW
    return scalar0


def bits_uand(x: Array) -> Array:
    if x.has_x():
        return scalarX
    if x.has_0():
        return scalar0
    if x.has_w():
        return scalarW
    return scalar1


def bits_uxor(x: Array) -> Array:
    if x.has_x():
        return scalarX
    if x.has_w():
        return scalarW
    return bool2scalar[x._data[1].bit_count() & 1]


# Arithmetic
def bits_add[T: Array](a: T, b: Array, ci: Array) -> tuple[T | Array, Array]:
    if a.size == b.size:
        t = resolve_type(a, b)
    else:
        t = vec_cls(max(a.size, b.size))

    # X/W propagation
    if a.has_x() or b.has_x() or ci.has_x():
        return t.xs(), scalarX
    if a.has_w() or b.has_w() or ci.has_w():
        return t.ws(), scalarW

    s1 = a._data[1] + b._data[1] + ci._data[1]
    co = bool2scalar[s1 > t._dmax]
    s1 &= t._dmax
    s0 = s1 ^ t._dmax

    return t._cast_data(s0, s1), co


def bits_inc[T: Array](a: T) -> tuple[T, Array]:
    # X/W propagation
    if a.has_x():
        return a.xs(), scalarX
    if a.has_w():
        return a.ws(), scalarW

    s1 = a._data[1] + 1
    co = bool2scalar[s1 > a._dmax]
    s1 &= a._dmax
    s0 = s1 ^ a._dmax

    return a._cast_data(s0, s1), co


def bits_sub[T: Array](a: T, b: Array) -> tuple[T | Array, Array]:
    return bits_add(a, bits_not(b), ci=scalar1)


def bits_neg[T: Array](x: T) -> tuple[T, Array]:
    return bits_inc(bits_not(x))


def bits_mul(a: Array, b: Array) -> Array:
    V = vec_cls(a.size + b.size)

    # X/W propagation
    if a.has_x() or b.has_x():
        return V.xs()
    if a.has_w() or b.has_w():
        return V.ws()

    p1 = a._data[1] * b._data[1]
    p0 = p1 ^ V._dmax

    return V(p0, p1)


def bits_div[T: Array](a: T, b: Array) -> T:
    if not a.size >= b.size > 0:
        raise ValueError("Expected a.size ≥ b.size > 0")

    # X/W propagation
    if a.has_x() or b.has_x():
        return a.xs()
    if a.has_w() or b.has_w():
        return a.ws()

    q1 = a._data[1] // b._data[1]
    q0 = q1 ^ a._dmax

    return a._cast_data(q0, q1)


def bits_mod[T: Array](a: Array, b: T) -> T:
    if not a.size >= b.size > 0:
        raise ValueError("Expected a.size ≥ b.size > 0")

    # X/W propagation
    if a.has_x() or b.has_x():
        return b.xs()
    if a.has_w() or b.has_w():
        return b.ws()

    r1 = a._data[1] % b._data[1]
    r0 = r1 ^ b._dmax

    return b._cast_data(r0, r1)


def _and_or(a: Array, b: Array) -> Array:
    return bits_uor(bits_and(a, b))


def bits_matmul(a: Array, b: Array) -> Array:
    match (a.shape, b.shape):
        # Vec[k] @ Vec[k] => Scalar
        case (int() as k1,), (int() as k2,) if k1 == k2:
            return _and_or(a, b)
        # Vec[k] @ Array[k,n] => Vec[n]
        case (int() as k1,), (int() as k2, int() as n) if k1 == k2:
            return _stack(*[_and_or(a, b[:, j]) for j in range(n)])
        # Array[m,k] @ Vec[k] => Vec[m]
        case (int() as m, int() as k1), (int() as k2,) if k1 == k2:
            return _stack(*[_and_or(a[i, :], b) for i in range(m)])
        # Array[m,k] @ Array[k,n] => Array[m,n]
        case (int() as m, int() as k1), (int() as k2, int() as n) if k1 == k2:
            xs = [_stack(*[_and_or(a[i, :], b[:, j]) for j in range(n)]) for i in range(m)]
            return _stack(*xs)
        # Incompatible shapes
        case _:
            s = "Expected Array[m,k] @ Array[k,n]"
            s += f", got {a.__class__.__name__} @ {b.__class__.__name__}"
            raise TypeError(s)


def bits_lsh[T: Array](x: T, n: Array) -> T:
    if n.has_x():
        return x.xs()
    if n.has_w():
        return x.ws()

    _n = n.to_uint()
    if _n == 0:
        return x
    if _n > x.size:
        raise ValueError(f"Expected n ≤ {x.size}, got {_n}")

    _, (sh0, sh1) = x._get_slice(0, x.size - _n)
    d0 = mask(_n) | sh0 << _n
    d1 = sh1 << _n
    y = x._cast_data(d0, d1)

    return y


def bits_rsh[T: Array](x: T, n: Array) -> T:
    if n.has_x():
        return x.xs()
    if n.has_w():
        return x.ws()

    _n = n.to_uint()
    if _n == 0:
        return x
    if _n > x.size:
        raise ValueError(f"Expected n ≤ {x.size}, got {_n}")

    sh_size, (sh0, sh1) = x._get_slice(_n, x.size)
    d0 = sh0 | (mask(_n) << sh_size)
    d1 = sh1
    y = x._cast_data(d0, d1)

    return y


# Word
def bits_cat(*xs: Array) -> Array:
    if len(xs) == 0:
        return empty_obj()
    if len(xs) == 1:
        return xs[0]

    size = 0
    d0, d1 = 0, 0
    for x in xs:
        d0 |= x._data[0] << size
        d1 |= x._data[1] << size
        size += x.size
    return vec_cls(size)(d0, d1)


def _bools2vec(x0: int, *xs: int) -> Array:
    """Convert an iterable of bools to a vec.

    This is a convenience function.
    For data in the form of [0, 1, 0, 1, ...],
    or [False, True, False, True, ...].
    """
    size = 1
    d1 = int(x0)
    for x in xs:
        if x in (0, 1):
            d1 |= x << size
        else:
            raise TypeError(f"Expected x in {{0, 1}}, got {x}")
        size += 1
    d0 = d1 ^ mask(size)
    return vec_obj(size, d0, d1)


def _rank2(fst: Array, *rst: VectorLike) -> Array:
    d0, d1 = fst._data
    for i, x in enumerate(rst, start=1):
        _x = expect_vec_size(x, fst.size)
        d0 |= _x._data[0] << (fst.size * i)
        d1 |= _x._data[1] << (fst.size * i)
    if fst.shape == (0,):
        return empty_obj()
    if fst.shape == (1,):
        size = len(rst) + 1
        return vec_obj(size, d0, d1)
    shape = (len(rst) + 1,) + fst.shape
    return array_obj(shape, d0, d1)


def bits(obj: Any = None) -> Array:
    """Create a shaped Array object using standard input formats.

    For example, empty input returns an ``Empty`` instance.

    >>> bits()
    bits([])
    >>> bits(None)
    bits([])

    ``bool``, ``int``, and string literal inputs:

    >>> bits(False)
    bits("1b0")
    >>> bits([False, True, False, True])
    bits("4b1010")
    >>> bits("8d42")
    bits("8b0010_1010")

    Use a ``list`` of inputs to create arbitrary shaped inputs:

    >>> x = bits([["2b00", "2b01"], ["2b10", "2b11"]])
    >>> x
    bits([["2b00", "2b01"],
          ["2b10", "2b11"]])
    >>> x.shape
    (2, 2, 2)

    Args:
        obj: Object that can be converted to an Array instance.

    Returns:
        Array instance.

    Raises:
        TypeError: If input obj is invalid.
    """
    match obj:
        case None | []:
            y = empty_obj()
        case 0 | 1:
            y = bool2scalar[obj]
        case [0 | 1 as fst, *rst]:
            y = _bools2vec(fst, *rst)
        case str() as lit:
            y = lit2bv(lit)
        case [str() as lit, *rst]:
            x = lit2bv(lit)
            y = _rank2(x, *rst)
        case [Array() as x, *rst]:
            y = _rank2(x, *rst)
        case [*objs]:
            y = _stack(*[bits(obj) for obj in objs])
        case _:
            raise TypeError(f"Invalid input: {obj}")

    return y


def _stack(*xs: Array) -> Array:
    if len(xs) == 0:
        return empty_obj()
    if len(xs) == 1:
        return xs[0]

    fst, rst = xs[0], xs[1:]

    size = fst.size
    d0, d1 = fst._data
    for x in rst:
        if x.shape != fst.shape:
            s = f"Expected shape {fst.shape}, got {x.shape}"
            raise TypeError(s)
        d0 |= x._data[0] << size
        d1 |= x._data[1] << size
        size += x.size

    # {Empty, Empty, ...} => Empty
    if fst.shape == (0,):
        return empty_obj()

    # {Scalar, Scalar, ...} => Vector[K]
    if fst.shape == (1,):
        size = len(xs)
        return vec_obj(size, d0, d1)

    # {Vector[K], Vector[K], ...} => Array[J,K]
    # {Array[J,K], Array[J,K], ...} => Array[I,J,K]
    shape = (len(xs),) + fst.shape
    return array_obj(shape, d0, d1)


def stack(*objs: ArrayLike) -> Array:
    """Stack a sequence of Arrays with same shape into a higher dimensional shape.

    For a sequence length N with shape M,
    the output shape will be M x N.

    For example, a sequence of scalars stacked to a vector:

    >>> stack(0, 1, 0, 1)
    bits("4b1010")

    Or a sequence of vectors stacked to an array:

    >>> x0 = stack("2b00", "2b01")
    >>> x1 = stack("2b10", "2b11")
    >>> y = stack(x0, x1)
    >>> y
    bits([["2b00", "2b01"],
          ["2b10", "2b11"]])
    >>> y.shape
    (2, 2, 2)

    Args:
        objs: a sequence of vec/bits/bool/lit objects.

    Returns:
        Array instance.

    Raises:
        TypeError: If input obj is invalid.
    """
    return _stack(*[expect_array(obj) for obj in objs])


def lit2bv(lit: str) -> Array:
    """Convert string literal to Vector.

    A string literal is in the form {width}{base}{characters},
    where width is the number of bits, base is either 'b' for binary or
    'h' for hexadecimal, and characters is a string of legal characters.
    The character string can contains '_' separators for readability.

    For example:

    * ``"4b1010"``
    * ``"6b11_-10X"``
    * ``"64hdead_beef_feed_face"``

    Returns:
        A Vec instance.

    Raises:
        ValueError: If input literal has a syntax error.
    """
    size, (d0, d1) = lb.parse_lit(lit)
    return vec_obj(size, d0, d1)


def u2bv(n: int, size: int | None = None) -> Array:
    """Convert nonnegative int to Vector.

    For example:

    >>> u2bv(42, size=8)
    bits("8b0010_1010")

    Args:
        n: Nonnegative ``int`` to convert.
        size: Optional ``int`` output size.
              Defaults to minimum required size.

    Returns:
        ``Vector``

    Raises:
        ValueError: ``n`` is negative or overflows the output size.
    """
    if n < 0:
        raise ValueError(f"Expected n ≥ 0, got {n}")

    # Compute required number of bits
    min_size = clog2(n + 1)
    if size is None:
        size = min_size
    elif size < min_size:
        s = f"Overflow: n = {n} required size ≥ {min_size}, got {size}"
        raise ValueError(s)

    d1 = n
    d0 = d1 ^ mask(size)

    return vec_obj(size, d0, d1)


def i2bv(n: int, size: int | None = None) -> Array:
    """Convert int to Vector.

    For example:

    >>> i2bv(42, size=8)
    bits("8b0010_1010")
    >>> i2bv(-42, size=8)
    bits("8b1101_0110")

    Args:
        n: ``int`` to convert.
        size: Optional ``int`` output size.
              Defaults to minimum required size.

    Returns:
        ``Vector``

    Raises:
        ValueError: ``n`` overflows the output size.
    """
    negative = n < 0
    d1 = abs(n)

    # Compute required number of bits
    if negative:
        min_size = clog2(d1) + 1
    else:
        min_size = clog2(d1 + 1) + 1

    if size is None:
        size = min_size
    elif size < min_size:
        s = f"Overflow: n = {n} required size ≥ {min_size}, got {size}"
        raise ValueError(s)

    if negative:
        d1 = (d1 ^ mask(size)) + 1

    d0 = d1 ^ mask(size)

    return vec_obj(size, d0, d1)


def _chunk(data: lbv, base: int, mask: int) -> lbv:
    return (data[0] >> base) & mask, (data[1] >> base) & mask


def _sel(x: Array, key: tuple[tuple[int, int], ...]) -> Array:
    assert len(x.shape) == len(key)

    (start, stop), key_r = key[0], key[1:]
    assert 0 <= start <= stop <= x.shape[0]

    # Partial select m:n
    if start != 0 or stop != x.shape[0]:
        if len(key_r) == 0:
            size = stop - start
            d0, d1 = _chunk(x._data, start, mask(size))
            return vec_obj(size, d0, d1)

        if len(key_r) == 1:
            V = vec_cls(x.shape[1])
            vecs: list[Array] = []
            for i in range(start, stop):
                d0, d1 = _chunk(x._data, V.size * i, V._dmax)
                vecs.append(V(d0, d1))
            return _stack(*[_sel(vec, key_r) for vec in vecs])

        A = array_cls(x.shape[1:])
        arrays: list[Array] = []
        for i in range(start, stop):
            d0, d1 = _chunk(x._data, A.size * i, A._dmax)
            arrays.append(A(d0, d1))
        return _stack(*[_sel(array, key_r) for array in arrays])

    # Full select 0:n
    if key_r:
        return _stack(*[_sel(x_r, key_r) for x_r in x])

    return x


def _norm_index(n: int, index: int) -> int:
    lo, hi = -n, n
    if not lo <= index < hi:
        s = f"Expected index in [{lo}, {hi}), got {index}"
        raise IndexError(s)
    # Normalize negative start index
    if index < 0:
        return index + hi
    return index


def _norm_slice(n: int, sl: KeySlice) -> tuple[int, int]:
    lo, hi = -n, n
    if sl.step is not None:
        raise ValueError("Slice step is not supported")
    # Normalize start index
    start = sl.start
    if start is None or start < lo:
        start = lo
    if start < 0:
        start += hi
    # Normalize stop index
    stop = sl.stop
    if stop is None or stop > hi:
        stop = hi
    if stop < 0:
        stop += hi
    # Clamp reverse slice to empty
    stop = max(start, stop)
    return start, stop


def _sep(indent: str, x: Array) -> str:
    # 2-D Matrix
    if len(x.shape) == 2:  # noqa: PLR2004
        return ", "
    # 3-D
    if len(x.shape) == 3:  # noqa: PLR2004
        return ",\n" + indent
    # N-D
    return ",\n\n" + indent


def _repr(indent: str, x: Array) -> str:
    # 1-D Vector
    if len(x.shape) == 1:
        return f'"{x}"'
    sep = _sep(indent, x)
    f = partial(_repr, indent + " ")
    return "[" + sep.join(map(f, x)) + "]"


def _str(indent: str, x: Array) -> str:
    # 1-D Vector
    if len(x.shape) == 1:
        return f"{x}"
    sep = _sep(indent, x)
    f = partial(_str, indent + " ")
    return "[" + sep.join(map(f, x)) + "]"
