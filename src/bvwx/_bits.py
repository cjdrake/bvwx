"""Bits Data Types"""

# PyLint is confused by my hacky classproperty implementation
# pylint: disable=comparison-with-callable
# pylint: disable=no-self-argument

# pylint: disable=protected-access

from __future__ import annotations

import math
import random
from collections.abc import Callable, Generator
from functools import cached_property, partial

from . import _lbool as lb
from ._lbool import lbv
from ._util import classproperty, clog2, mask

_VectorSize: dict[int, type[Vector]] = {}


def _get_vec_size(size: int) -> type[Vector]:
    """Return Vector[size] type."""
    assert isinstance(size, int) and size > 1
    try:
        return _VectorSize[size]
    except KeyError:
        name = f"Vector[{size}]"
        vec = type(name, (Vector,), {"_size": size})
        _VectorSize[size] = vec
        return vec


def vec_size(size: int) -> type[Vector]:
    """Vector[size] class factory."""
    assert size >= 0
    # Degenerate case: Null
    if size == 0:
        return Empty
    # Degenerate case: 0-D
    if size == 1:
        return Scalar
    # General case: 1-D
    return _get_vec_size(size)


_ArrayShape: dict[tuple[int, ...], type[Array]] = {}


def _get_array_shape(shape: tuple[int, ...]) -> type[Array]:
    """Return Array[shape] type."""
    assert len(shape) > 1 and all(isinstance(n, int) and n > 1 for n in shape)
    try:
        return _ArrayShape[shape]
    except KeyError:
        name = f'Array[{",".join(str(n) for n in shape)}]'
        size = math.prod(shape)
        array = type(name, (Array,), {"_shape": shape, "_size": size})
        _ArrayShape[shape] = array
        return array


def expect_bits(arg: BitsLike) -> Bits:
    """Any Bits-like object that defines its own size"""
    if arg in (0, 1):
        return bool2scalar[arg]
    if isinstance(arg, str):
        return lit2bv(arg)
    if isinstance(arg, Bits):
        return arg
    raise TypeError("Expected arg to be: Bits, str literal, or {0, 1}")


def expect_array(arg: ArrayLike) -> Array:
    """Any Array-like object that defines its own size"""
    if arg in (0, 1):
        return bool2scalar[arg]
    if isinstance(arg, str):
        return lit2bv(arg)
    if isinstance(arg, (Empty, Scalar, Vector, Array)):
        return arg
    raise TypeError("Expected arg to be: Array, str literal, or {0, 1}")


def expect_scalar(arg: ScalarLike) -> Scalar:
    """Any Scalar-like object"""
    if arg in (0, 1):
        return bool2scalar[arg]
    if isinstance(arg, str):
        return _expect_size(lit2bv(arg), 1)
    if isinstance(arg, Scalar):
        return arg
    raise TypeError("Expected arg to be: Scalar, str literal, or {0, 1}")


def expect_uint(arg: UintLike) -> Bits:
    """Any Bits-like object that defines its own size"""
    if isinstance(arg, int):
        return u2bv(arg)
    if isinstance(arg, str):
        return lit2bv(arg)
    if isinstance(arg, Bits):
        return arg
    raise TypeError("Expected arg to be: Bits, str literal, or {0, 1}")


def expect_bits_size(arg: BitsLike, size: int) -> Bits:
    """Any Bits-Like object that may or may not define its own size"""
    if isinstance(arg, int):
        if arg < 0:
            return i2bv(arg, size)
        return u2bv(arg, size)
    if isinstance(arg, str):
        return _expect_size(lit2bv(arg), size)
    if isinstance(arg, Bits):
        return _expect_size(arg, size)
    raise TypeError("Expected arg to be: Bits, str literal, or int")


def _expect_vec_size(arg: VectorLike, size: int) -> Bits:
    """Any Vector-Like object that may or may not define its own size"""
    if isinstance(arg, int):
        if arg < 0:
            return i2bv(arg, size)
        return u2bv(arg, size)
    if isinstance(arg, str):
        return _expect_size(lit2bv(arg), size)
    if isinstance(arg, (Empty, Scalar, Vector)):
        return _expect_size(arg, size)
    raise TypeError("Expected arg to be: Vector, str literal, or int")


def _expect_size(arg: Bits, size: int) -> Bits:
    if arg.size != size:
        raise TypeError(f"Expected size {size}, got {arg.size}")
    return arg


def resolve_type(t0: type[Bits], t1: type[Bits]) -> type[Bits]:
    # T (op) T -> T
    if t0 == t1:
        return t0

    # Otherwise, downgrade to Scalar/Vector
    return vec_size(t0.size)


class _SizedIf:

    _size: int

    @classproperty
    def size(cls) -> int:
        raise NotImplementedError()  # pragma: no cover


class _ShapedIf:

    _shape: tuple[int, ...]

    @classproperty
    def shape(cls) -> tuple[int, ...]:
        raise NotImplementedError()  # pragma: no cover


class Bits(_SizedIf):
    r"""Sequence of bits.

    A bit is a 4-state logical value in the set {``0``, ``1``, ``X``, ``-``}:

        * ``0`` is Boolean zero or "False"
        * ``1`` is Boolean one or "True"
        * ``X`` is an uninitialized or metastable value
        * ``-`` is a "don't care" value

    The values ``0`` and ``1`` are "known".
    The values ``X`` and ``-`` are "unknown".

    ``Bits`` is the base class for a family of hardware-oriented data types.
    All ``Bits`` objects have a ``size`` attribute.
    Shaped subclasses (``Empty``, ``Scalar``, ``Vector``, ``Array``) have a
    ``shape`` attribute.
    Composite subclasses (``Struct``, ``Union``) have user-defined attributes.

    ``Bits`` does **NOT** implement the Python ``Sequence`` protocol.

    Children::

                                 Bits
                                   |
                   +---------------+---------------+
                   |                               |
                Shaped                         Composite
                   |                               |
          +--------+--------+-------+         +----+----+
          |        |        |       |         |         |
        Array > Vector > Scalar > Empty    Struct     Union
                   |
                 Enum

    Do **NOT** construct a Bits object directly.
    Use one of the factory functions:

        * ``bits``
        * ``stack``
        * ``u2bv``
        * ``i2bv``
    """

    @classmethod
    def cast(cls, x: Bits) -> Bits:
        """Convert Bits object to an instance of this class.

        For example, to cast an ``Array[2,2]`` to a ``Vector[4]``:

        >>> x = bits(["2b00", "2b11"])
        >>> Vector[4].cast(x)
        bits("4b1100")

        Raises:
            TypeError: Object size does not match this class size.
        """
        if x.size != cls.size:
            raise TypeError(f"Expected size {cls.size}, got {x.size}")
        return cls._cast_data(x.data[0], x.data[1])

    @classmethod
    def _cast_data(cls, d0: int, d1: int) -> Bits:
        obj = object.__new__(cls)
        obj._data = (d0, d1)
        return obj

    @classmethod
    def xes(cls) -> Bits:
        """Return an instance filled with ``X`` bits.

        For example:

        >>> Vector[4].xes()
        bits("4bXXXX")
        """
        return cls._cast_data(0, 0)

    @classmethod
    def zeros(cls) -> Bits:
        """Return an instance filled with ``0`` bits.

        For example:

        >>> Vector[4].zeros()
        bits("4b0000")
        """
        return cls._cast_data(cls._dmax, 0)

    @classmethod
    def ones(cls) -> Bits:
        """Return an instance filled with ``1`` bits.

        For example:

        >>> Vector[4].ones()
        bits("4b1111")
        """
        return cls._cast_data(0, cls._dmax)

    @classmethod
    def dcs(cls) -> Bits:
        """Return an instance filled with ``-`` bits.

        For example:

        >>> Vector[4].dcs()
        bits("4b----")
        """
        return cls._cast_data(cls._dmax, cls._dmax)

    @classmethod
    def rand(cls) -> Bits:
        """Return an instance filled with random bits."""
        d1 = random.getrandbits(cls.size)
        return cls._cast_data(cls._dmax ^ d1, d1)

    @classmethod
    def xprop(cls, sel: Bits) -> Bits:
        """Propagate ``X`` in a wildcard pattern (default case).

        If ``sel`` contains an ``X``, propagate ``X``.
        Otherwise, treat as a "don't care", and propagate ``-``.

        For example:

        >>> def f(x: Vector[1]) -> Vector[1]:
        ...     match x:
        ...         case "1b0":
        ...             return bits("1b1")
        ...         case _:
        ...             return Vector[1].xprop(x)

        >>> f(bits("1b0"))  # Match!
        bits("1b1")
        >>> f(bits("1b1"))  # No match; No X prop
        bits("1b-")
        >>> f(bits("1bX"))  # No match; Yes X prop
        bits("1bX")

        Args:
            sel: Bits object, typically a ``match`` subject

        Returns:
            Class instance filled with either ``-`` or ``X``.
        """
        if sel._has_x:
            return cls.xes()
        return cls.dcs()

    @classproperty
    def _dmax(cls) -> int:
        return mask(cls.size)

    @property
    def data(self) -> tuple[int, int]:
        """Internal representation."""
        return self._data

    def __bool__(self) -> bool:
        """Convert to Python ``bool``.

        A ``Bits`` object is ``True`` if its value is known nonzero.

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

    # Comparison
    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, str):
            size, data = lb.parse_lit(obj)
            return self.size == size and self._data == data
        if isinstance(obj, Bits):
            return self.size == obj.size and self._data == obj.data
        return False

    def __hash__(self) -> int:
        return hash(self.shape) ^ hash(self._data)

    # Bitwise Operations
    def __invert__(self) -> Bits:
        return _not_(self)

    def __or__(self, other: BitsLike) -> Bits:
        other = expect_bits_size(other, self.size)
        return _or_(self, other)

    def __ror__(self, other: BitsLike) -> Bits:
        other = expect_bits_size(other, self.size)
        return _or_(other, self)

    def __and__(self, other: BitsLike) -> Bits:
        other = expect_bits_size(other, self.size)
        return _and_(self, other)

    def __rand__(self, other: BitsLike) -> Bits:
        other = expect_bits_size(other, self.size)
        return _and_(other, self)

    def __xor__(self, other: BitsLike) -> Bits:
        other = expect_bits_size(other, self.size)
        return _xor_(self, other)

    def __rxor__(self, other: BitsLike) -> Bits:
        other = expect_bits_size(other, self.size)
        return _xor_(other, self)

    # Note: Drop carry-out
    def __lshift__(self, n: UintLike) -> Bits:
        n = expect_uint(n)
        return _lsh(self, n)

    def __rlshift__(self, other: BitsLike) -> Bits:
        other = expect_bits(other)
        return _lsh(other, self)

    # Note: Drop carry-out
    def __rshift__(self, n: UintLike) -> Bits:
        n = expect_uint(n)
        return _rsh(self, n)

    def __rrshift__(self, other: BitsLike) -> Bits:
        other = expect_bits(other)
        return _rsh(other, self)

    # Note: Keep carry-out
    def __add__(self, other: BitsLike) -> Vector:
        other = expect_bits(other)
        s, co = _add(self, other, scalar0)
        return _cat(s, co)

    def __radd__(self, other: BitsLike) -> Vector:
        other = expect_bits(other)
        s, co = _add(other, self, scalar0)
        return _cat(s, co)

    # Note: Keep carry-out
    def __sub__(self, other: BitsLike) -> Vector:
        other = expect_bits_size(other, self.size)
        s, co = _sub(self, other)
        return _cat(s, co)

    def __rsub__(self, other: BitsLike) -> Vector:
        other = expect_bits_size(other, self.size)
        s, co = _sub(other, self)
        return _cat(s, co)

    # Note: Keep carry-out
    def __neg__(self) -> Vector:
        s, co = _neg(self)
        return _cat(s, co)

    def __mul__(self, other: BitsLike) -> Vector:
        other = expect_bits(other)
        return _mul(self, other)

    def __rmul__(self, other: BitsLike) -> Vector:
        other = expect_bits(other)
        return _mul(other, self)

    def __floordiv__(self, other: BitsLike) -> Bits:
        other = expect_bits(other)
        return _div(self, other)

    def __rfloordiv__(self, other: BitsLike) -> Bits:
        other = expect_bits(other)
        return _div(other, self)

    def __mod__(self, other: BitsLike) -> Bits:
        other = expect_bits(other)
        return _mod(self, other)

    # Note: __rmod__ does not work b/c str implements % operator

    def __matmul__(self, other: ArrayLike) -> Bits:
        other = expect_array(other)
        return _matmul(self, other)

    def __rmatmul__(self, other: ArrayLike) -> Bits:
        other = expect_array(other)
        return _matmul(other, self)

    def to_uint(self) -> int:
        """Convert to unsigned integer.

        Returns:
            A non-negative ``int``.

        Raises:
            ValueError: Contains any unknown bits.
        """
        if self.has_unknown():
            raise ValueError("Cannot convert unknown to uint")
        return self._data[1]

    def to_int(self) -> int:
        """Convert to signed integer.

        Returns:
            An ``int``, from two's complement encoding.

        Raises:
            ValueError: Contains any unknown bits.
        """
        if self.size == 0:
            return 0
        sign = self._get_index(self.size - 1)
        if sign == lb._1:
            return -(_not_(self).to_uint() + 1)
        return self.to_uint()

    def count_zeros(self) -> int:
        """Return count of of ``0`` bits."""
        d: int = self._data[0] & (self._data[1] ^ self._dmax)
        return d.bit_count()

    def count_ones(self) -> int:
        """Return count of ``1`` bits."""
        d: int = (self._data[0] ^ self._dmax) & self._data[1]
        return d.bit_count()

    def count_xes(self) -> int:
        """Return count of ``X`` bits."""
        d: int = (self._data[0] | self._data[1]) ^ self._dmax
        return d.bit_count()

    def count_dcs(self) -> int:
        """Return count of ``-`` bits."""
        d: int = self._data[0] & self._data[1]
        return d.bit_count()

    def count_unknown(self) -> int:
        """Return count of unknown bits."""
        d: int = self._data[0] ^ self._data[1] ^ self._dmax
        return d.bit_count()

    def onehot(self) -> bool:
        """Return True if contains exactly one ``1`` bit."""
        return not self.has_unknown() and self.count_ones() == 1

    def onehot0(self) -> bool:
        """Return True if contains at most one ``1`` bit."""
        return not self.has_unknown() and self.count_ones() <= 1

    @cached_property
    def _has_0(self) -> bool:
        return bool(self._data[0] & (self._data[1] ^ self._dmax))

    @cached_property
    def _has_1(self) -> bool:
        return bool((self._data[0] ^ self._dmax) & self._data[1])

    @cached_property
    def _has_x(self) -> bool:
        return bool((self._data[0] | self._data[1]) ^ self._dmax)

    @cached_property
    def _has_w(self) -> bool:
        return bool(self._data[0] & self._data[1])

    @cached_property
    def _has_xw(self) -> bool:
        return bool(self._data[0] ^ self._data[1] ^ self._dmax)

    def has_0(self) -> bool:
        """Return True if contains at least one ``0`` bit."""
        return self._has_0

    def has_1(self) -> bool:
        """Return True if contains at least one ``1`` bit."""
        return self._has_1

    def has_x(self) -> bool:
        """Return True if contains at least one ``X`` bit."""
        return self._has_x

    def has_dc(self) -> bool:
        """Return True if contains at least one ``-`` bit."""
        return self._has_w

    def has_unknown(self) -> bool:
        """Return True if contains at least one unknown bit."""
        return self._has_xw

    def vcd_var(self) -> str:
        """Return VCD variable type."""
        return "logic"

    def vcd_val(self) -> str:
        """Return VCD variable value."""
        return "".join(lb.to_vcd_char[self._get_index(i)] for i in range(self.size - 1, -1, -1))

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

    def _get_key(self, key: Key) -> tuple[int, lbv]:
        if isinstance(key, int):
            index = _norm_index(self.size, key)
            return 1, self._get_index(index)
        if isinstance(key, slice):
            start, stop = _norm_slice(self.size, key)
            if start != 0 or stop != self.size:
                return self._get_slice(start, stop)
            return self.size, self._data
        if isinstance(key, str):
            key = lit2bv(key)
            index = _norm_index(self.size, key.to_uint())
            return 1, self._get_index(index)
        if isinstance(key, Bits):
            index = _norm_index(self.size, key.to_uint())
            return 1, self._get_index(index)
        raise TypeError("Expected key to be int, slice, str literal, or Bits")


class Array(Bits, _ShapedIf):
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

    def __class_getitem__(cls, shape: int | tuple[int, ...]) -> type[Array]:
        if isinstance(shape, int):
            return vec_size(shape)
        if isinstance(shape, tuple) and all(isinstance(n, int) and n > 1 for n in shape):
            return _get_array_shape(shape)
        raise TypeError(f"Invalid shape parameter: {shape}")

    def __new__(cls, d0: int, d1: int) -> Array:
        return cls._cast_data(d0, d1)

    @classproperty
    def size(cls) -> int:
        return cls._size

    @classproperty
    def shape(cls) -> tuple[int, ...]:
        return cls._shape

    def __repr__(self) -> str:
        prefix = "bits"
        indent = " " * len(prefix) + "  "
        return f"{prefix}({_array_repr(indent, self)})"

    def __str__(self) -> str:
        indent = " "
        return f"{_array_str(indent, self)}"

    def __getitem__(self, key: Key | tuple[Key, ...]) -> Array:
        if isinstance(key, (int, slice, Bits, str)):
            nkey = self._norm_key([key])
            return _sel(self, nkey)
        if isinstance(key, tuple):
            nkey = self._norm_key(list(key))
            return _sel(self, nkey)
        s = "Expected key to be int, slice, or tuple[int | slice, ...]"
        raise TypeError(s)

    def __iter__(self) -> Generator[Array, None, None]:
        for i in range(self._shape[0]):
            yield self[i]

    def reshape(self, shape: tuple[int, ...]) -> Array:
        if shape == self.shape:
            return self
        if math.prod(shape) != self._size:
            s = f"Expected shape with size {self._size}, got {shape}"
            raise ValueError(s)
        if len(shape) == 1:
            return _get_vec_size(shape[0])(self._data[0], self._data[1])
        return _get_array_shape(shape)(self._data[0], self._data[1])

    def flatten(self) -> Vector:
        return _get_vec_size(self._size)(self._data[0], self._data[1])

    @classmethod
    def _norm_key(cls, keys: list[Key]) -> tuple[tuple[int, int], ...]:
        ndim = len(cls._shape)
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
            if isinstance(key, slice):
                return _norm_slice(n, key)
            if isinstance(key, str):
                key = lit2bv(key)
                i = _norm_index(n, key.to_uint())
                return (i, i + 1)
            if isinstance(key, Bits):
                i = _norm_index(n, key.to_uint())
                return (i, i + 1)
            assert False  # pragma: no cover

        return tuple(f(n, key) for n, key in zip(cls._shape, keys))


class Vector(Bits, _ShapedIf):
    """One dimensional sequence of bits.

    To create a ``Vector`` instance,
    use binary, decimal, or hexadecimal string literals:

    >>> bits("4b1010")
    bits("4b1010")
    >>> bits("4d10")
    bits("4b1010")
    >>> bits("4ha")
    bits("4b1010")

    ``Vector`` implements ``size`` and ``shape`` attributes,
    as well as ``__len__`` and ``__getitem__`` methods:

    >>> x = bits("8b1111_0000")
    >>> x.size
    8
    >>> x.shape
    (8,)
    >>> len(x)
    8
    >>> x[3]
    bits("1b0")
    >>> x[4]
    bits("1b1")
    >>> x[2:6]
    bits("4b1100")

    A ``Vector`` may be converted into an equal-size multi-dimensional ``Array``
    using the ``reshape`` method:

    >>> x.reshape((2,4))
    bits(["4b0000", "4b1111"])
    """

    def __class_getitem__(cls, size: int) -> type[Vector]:
        if isinstance(size, int) and size >= 0:
            return vec_size(size)
        raise TypeError(f"Invalid size parameter: {size}")

    def __new__(cls, d0: int, d1: int) -> Vector:
        return cls._cast_data(d0, d1)

    @classproperty
    def size(cls) -> int:
        return cls._size

    @classproperty
    def shape(cls) -> tuple[int, ...]:
        return (cls._size,)

    def __repr__(self) -> str:
        return f'bits("{self.__str__()}")'

    def __str__(self) -> str:
        prefix = f"{self.size}b"
        chars = [lb.to_char[self._get_index(0)]]
        for i in range(1, self.size):
            if i % 4 == 0:
                chars.append("_")
            chars.append(lb.to_char[self._get_index(i)])
        return prefix + "".join(reversed(chars))

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, key: Key) -> Vector:
        size, (d0, d1) = self._get_key(key)
        return vec_size(size)(d0, d1)

    def __iter__(self) -> Generator[Scalar, None, None]:
        for i in range(self._size):
            yield _scalars[self._get_index(i)]

    def reshape(self, shape: tuple[int, ...]) -> Array:
        if shape == self.shape:
            return self
        if math.prod(shape) != self.size:
            s = f"Expected shape with size {self.size}, got {shape}"
            raise ValueError(s)
        return _get_array_shape(shape)(self._data[0], self._data[1])

    def flatten(self) -> Vector:
        return self


class Scalar(Bits, _ShapedIf):
    """Zero dimensional (scalar) sequence of bits.

    Degenerate form of a ``Vector`` resulting from a one bit slice.

    >>> from bvwx import Vec
    >>> Vec[1] is Scalar
    True

    To get a handle to a ``Scalar`` instance:

    >>> f = bits("1b0")
    >>> t = bits("1b1")
    >>> x = bits("1bX")
    >>> dc = bits("1b-")

    For convenience, ``False`` and ``True`` also work:

    >>> bits(False) is f and bits(True) is t
    True

    ``Scalar`` implements ``Vector`` methods,
    including ``__getitem__``:

    >>> t.size
    1
    >>> t.shape
    (1,)
    >>> len(t)
    1
    >>> t[0]
    bits("1b1")
    """

    def __new__(cls, d0: int, d1: int):
        return _scalars[(d0, d1)]

    @classproperty
    def size(cls) -> int:
        return 1

    @classproperty
    def shape(cls) -> tuple[int, ...]:
        return (1,)

    def __repr__(self) -> str:
        return f'bits("{self.__str__()}")'

    def __str__(self) -> str:
        return f"1b{lb.to_char[self._data]}"

    def __len__(self) -> int:
        return 1

    def __getitem__(self, key: Key) -> Scalar:
        size, (d0, d1) = self._get_key(key)
        return vec_size(size)(d0, d1)

    def __iter__(self) -> Generator[Scalar, None, None]:
        yield self


scalarX = Scalar._cast_data(*lb._X)
scalar0 = Scalar._cast_data(*lb._0)
scalar1 = Scalar._cast_data(*lb._1)
scalarW = Scalar._cast_data(*lb._W)

_scalars = {
    lb._X: scalarX,
    lb._0: scalar0,
    lb._1: scalar1,
    lb._W: scalarW,
}
bool2scalar = (scalar0, scalar1)


class Empty(Bits, _ShapedIf):
    """Null dimensional sequence of bits.

    Degenerate form of a ``Vector`` resulting from an empty slice.

    >>> from bvwx import Vec
    >>> Vec[0] is Empty
    True

    To get a handle to an ``Empty`` instance:

    >>> empty = bits()

    ``Empty`` implements ``Vector`` methods,
    but __getitem__ will always raise an exception:

    >>> empty.size
    0
    >>> empty.shape
    (0,)
    >>> len(empty)
    0
    >>> empty[0]
    Traceback (most recent call last):
        ...
    IndexError: Expected index in [0, 0), got 0
    """

    def __new__(cls, d0: int, d1: int):
        assert d0 == d1 == 0
        return _empty

    def __reversed__(self):
        yield self

    @classproperty
    def size(cls) -> int:
        return 0

    @classproperty
    def shape(cls) -> tuple[int, ...]:
        return (0,)

    def __repr__(self) -> str:
        return "bits([])"

    def __str__(self) -> str:
        return "[]"

    def __len__(self) -> int:
        return 0

    def __getitem__(self, key: Key) -> Empty:
        # This will always raise an exception
        _ = self._get_key(key)

    def __iter__(self) -> Generator[Scalar, None, None]:
        yield from ()


_empty = Empty._cast_data(0, 0)


# Type Aliases
type BitsLike = Bits | str | int
type ArrayLike = Array | str | int
type VectorLike = Vector | str | int
type ScalarLike = Scalar | str | int
type UintLike = Bits | str | int
type Key = int | slice | Bits | str


# Bitwise
def _not_(x: Bits) -> Bits:
    d0, d1 = lb.not_(x.data)
    return x._cast_data(d0, d1)


def _or_(x0: Bits, x1: Bits) -> Bits:
    d0, d1 = lb.or_(x0.data, x1.data)
    t = resolve_type(type(x0), type(x1))
    return t._cast_data(d0, d1)


def _and_(x0: Bits, x1: Bits) -> Bits:
    d0, d1 = lb.and_(x0.data, x1.data)
    t = resolve_type(type(x0), type(x1))
    return t._cast_data(d0, d1)


def _xnor_(x0: Bits, x1: Bits) -> Bits:
    d0, d1 = lb.xnor(x0.data, x1.data)
    t = resolve_type(type(x0), type(x1))
    return t._cast_data(d0, d1)


def _xor_(x0: Bits, x1: Bits) -> Bits:
    d0, d1 = lb.xor(x0.data, x1.data)
    t = resolve_type(type(x0), type(x1))
    return t._cast_data(d0, d1)


def _impl_(p: Bits, q: Bits) -> Bits:
    d0, d1 = lb.impl(p.data, q.data)
    t = resolve_type(type(p), type(q))
    return t._cast_data(d0, d1)


def _ite_(s: Bits, x1: Bits, x0: Bits) -> Bits:
    s0 = mask(x1.size) * s.data[0]
    s1 = mask(x1.size) * s.data[1]
    d0, d1 = lb.ite((s0, s1), x1.data, x0.data)
    t = resolve_type(type(x0), type(x1))
    return t._cast_data(d0, d1)


def _mux_(s: Bits, t: type[Bits], xs: dict[int, Bits]) -> Bits:
    m = mask(t.size)
    si = (s._get_index(i) for i in range(s.size))
    s = tuple((m * d0, m * d1) for d0, d1 in si)
    dc = t.dcs()
    d0, d1 = lb.mux(s, {i: x.data for i, x in xs.items()}, dc.data)
    return t._cast_data(d0, d1)


# Logical
def _lor_(*xs: Scalar) -> Scalar:
    y = lb._0
    for x in xs:
        y = lb.or_(y, x.data)
    return _scalars[y]


def _land_(*xs: Scalar) -> Scalar:
    y = lb._1
    for x in xs:
        y = lb.and_(y, x.data)
    return _scalars[y]


def _lxor_(*xs: Scalar) -> Scalar:
    y = lb._0
    for x in xs:
        y = lb.xor(y, x.data)
    return _scalars[y]


# Unary
def _uor(x: Bits) -> Scalar:
    if x._has_x:
        return scalarX
    if x._has_1:
        return scalar1
    if x._has_w:
        return scalarW
    return scalar0


def _uand(x: Bits) -> Scalar:
    if x._has_x:
        return scalarX
    if x._has_0:
        return scalar0
    if x._has_w:
        return scalarW
    return scalar1


def _uxor(x: Bits) -> Scalar:
    if x._has_x:
        return scalarX
    if x._has_w:
        return scalarW
    return bool2scalar[x.data[1].bit_count() & 1]


# Arithmetic
def _add(a: Bits, b: Bits, ci: Scalar) -> tuple[Bits, Scalar]:
    if a.size == b.size:
        t = resolve_type(type(a), type(b))
    else:
        t = vec_size(max(a.size, b.size))

    # X/DC propagation
    if a._has_x or b._has_x or ci._has_x:
        return t.xes(), scalarX
    if a._has_w or b._has_w or ci._has_w:
        return t.dcs(), scalarW

    dmax = mask(t.size)
    s = a.data[1] + b.data[1] + ci.data[1]
    co = bool2scalar[s > dmax]
    s &= dmax

    return t._cast_data(s ^ dmax, s), co


def _inc(a: Bits) -> tuple[Bits, Scalar]:
    # X/DC propagation
    if a._has_x:
        return a.xes(), scalarX
    if a._has_w:
        return a.dcs(), scalarW

    dmax = mask(a.size)
    s = a.data[1] + 1
    co = bool2scalar[s > dmax]
    s &= dmax

    return a._cast_data(s ^ dmax, s), co


def _sub(a: Bits, b: Bits) -> tuple[Bits, Scalar]:
    return _add(a, _not_(b), ci=scalar1)


def _neg(x: Bits) -> tuple[Bits, Scalar]:
    return _inc(_not_(x))


def _mul(a: Bits, b: Bits) -> Vector:
    t = vec_size(a.size + b.size)

    # X/DC propagation
    if a._has_x or b._has_x:
        return t.xes()
    if a._has_w or b._has_w:
        return t.dcs()

    dmax = mask(t.size)
    p = a.data[1] * b.data[1]

    return t(p ^ dmax, p)


def _div(a: Bits, b: Bits) -> Bits:
    if not a.size >= b.size > 0:
        raise ValueError("Expected a.size ≥ b.size > 0")

    # X/DC propagation
    if a._has_x or b._has_x:
        return a.xes()
    if a._has_w or b._has_w:
        return a.dcs()

    dmax = mask(a.size)
    q = a.data[1] // b.data[1]

    return a._cast_data(q ^ dmax, q)


def _mod(a: Bits, b: Bits) -> Bits:
    if not a.size >= b.size > 0:
        raise ValueError("Expected a.size ≥ b.size > 0")

    # X/DC propagation
    if a._has_x or b._has_x:
        return b.xes()
    if a._has_w or b._has_w:
        return b.dcs()

    dmax = mask(b.size)
    r = a.data[1] % b.data[1]

    return b._cast_data(r ^ dmax, r)


def _and_or(a: Vector, b: Vector) -> Scalar:
    return _uor(_and_(a, b))


def _matmul(a: Array, b: Array) -> Array:
    match (a.shape, b.shape):
        # Vec[n] @ Vec[n] => Scalar
        case (int() as n1,), (int() as n2,) if n1 == n2:
            return _and_or(a, b)
        # Vec[m] @ Array[m,n] => Vec[n]
        case (int() as m1,), (int() as m2, int() as n) if m1 == m2:
            return _stack(*[_and_or(a, b[:, j]) for j in range(n)])
        # Array[m,n] @ Vec[n] => Vec[m]
        case (int() as m, int() as n1), (int() as n2,) if n1 == n2:
            return _stack(*[_and_or(a[i, :], b) for i in range(m)])
        # Array[m,n] @ Array[n,p] => Array[m,p]
        case (int() as m, int() as n1), (int() as n2, int() as p) if n1 == n2:
            xs = [_stack(*[_and_or(a[i, :], b[:, j]) for j in range(p)]) for i in range(m)]
            return _stack(*xs)
        # Incompatible shapes
        case _:
            s = "Expected Array[m,n] @ Array[n,p]"
            s += f", got {a.__class__.__name__} @ {b.__class__.__name__}"
            raise TypeError(s)


def _lsh(x: Bits, n: Bits) -> Bits:
    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x
    if n > x.size:
        raise ValueError(f"Expected n ≤ {x.size}, got {n}")

    _, (sh0, sh1) = x._get_slice(0, x.size - n)
    d0 = mask(n) | sh0 << n
    d1 = sh1 << n
    y = x._cast_data(d0, d1)

    return y


def _rsh(x: Bits, n: Bits) -> Bits:
    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x
    if n > x.size:
        raise ValueError(f"Expected n ≤ {x.size}, got {n}")

    sh_size, (sh0, sh1) = x._get_slice(n, x.size)
    d0 = sh0 | (mask(n) << sh_size)
    d1 = sh1
    y = x._cast_data(d0, d1)

    return y


def _srsh(x: Bits, n: Bits) -> Bits:
    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x
    if n > x.size:
        raise ValueError(f"Expected n ≤ {x.size}, got {n}")

    sign0, sign1 = x._get_index(x.size - 1)
    si0, si1 = mask(n) * sign0, mask(n) * sign1

    sh_size, (sh0, sh1) = x._get_slice(n, x.size)
    d0 = sh0 | si0 << sh_size
    d1 = sh1 | si1 << sh_size
    y = x._cast_data(d0, d1)

    return y


# Word
def _xt(x: Bits, n: Bits) -> Vector:
    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x

    ext0 = mask(n)
    d0 = x.data[0] | ext0 << x.size
    d1 = x.data[1]
    return vec_size(x.size + n)(d0, d1)


def _sxt(x: Bits, n: Bits) -> Vector:
    # Empty does not have a sign
    if x.size == 0:
        raise TypeError("Cannot sign extend empty")

    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x

    sign0, sign1 = x._get_index(x.size - 1)
    ext0 = mask(n) * sign0
    ext1 = mask(n) * sign1
    d0 = x.data[0] | ext0 << x.size
    d1 = x.data[1] | ext1 << x.size
    return vec_size(x.size + n)(d0, d1)


def _lrot(x: Bits, n: Bits) -> Bits:
    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x
    if n >= x.size:
        raise ValueError(f"Expected n < {x.size}, got {n}")

    _, (co0, co1) = x._get_slice(x.size - n, x.size)
    _, (sh0, sh1) = x._get_slice(0, x.size - n)
    d0 = co0 | sh0 << n
    d1 = co1 | sh1 << n
    return x._cast_data(d0, d1)


def _rrot(x: Bits, n: Bits) -> Bits:
    if n._has_x:
        return x.xes()
    if n._has_w:
        return x.dcs()

    n = n.to_uint()
    if n == 0:
        return x
    if n >= x.size:
        raise ValueError(f"Expected n < {x.size}, got {n}")

    _, (co0, co1) = x._get_slice(0, n)
    sh_size, (sh0, sh1) = x._get_slice(n, x.size)
    d0 = sh0 | co0 << sh_size
    d1 = sh1 | co1 << sh_size
    return x._cast_data(d0, d1)


def _cat(*xs: Bits) -> Vector:
    if len(xs) == 0:
        return _empty
    if len(xs) == 1:
        return xs[0]

    size = 0
    d0, d1 = 0, 0
    for x in xs:
        d0 |= x.data[0] << size
        d1 |= x.data[1] << size
        size += x.size
    return vec_size(size)(d0, d1)


def _pack(x: Bits, n: int) -> Bits:
    if n < 1:
        raise ValueError(f"Expected n ≥ 1, got {n}")
    if x.size % n != 0:
        raise ValueError("Expected x.size to be a multiple of n")

    if x.size == 0:
        return x

    m = mask(n)
    xd0, xd1 = x.data
    d0, d1 = xd0 & m, xd1 & m
    for _ in range(n, x.size, n):
        xd0 >>= n
        xd1 >>= n
        d0 = (d0 << n) | (xd0 & m)
        d1 = (d1 << n) | (xd1 & m)

    return x._cast_data(d0, d1)


# Predicates over bitvectors
def _eq(x0: Bits, x1: Bits) -> Scalar:
    return _uand(_xnor_(x0, x1))


def _ne(x0: Bits, x1: Bits) -> Scalar:
    return _uor(_xor_(x0, x1))


def _cmp(op: Callable, x0: Bits, x1: Bits) -> Scalar:
    # X/DC propagation
    if x0._has_x or x1._has_x:
        return scalarX
    if x0._has_w or x1._has_w:
        return scalarW
    return bool2scalar[op(x0.to_uint(), x1.to_uint())]


def _scmp(op: Callable, x0: Bits, x1: Bits) -> Scalar:
    # X/DC propagation
    if x0._has_x or x1._has_x:
        return scalarX
    if x0._has_w or x1._has_w:
        return scalarW
    return bool2scalar[op(x0.to_int(), x1.to_int())]


def _match(x0: Bits, x1: Bits) -> Scalar:
    # Propagate X
    if x0._has_x or x1._has_x:
        return scalarX

    for i in range(x0.size):
        a0, a1 = x0._get_index(i)
        b0, b1 = x1._get_index(i)
        if a0 ^ b0 and a1 ^ b1:
            return scalar0
    return scalar1


def _bools2vec(x0: int, *xs: int) -> Vector:
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
    return vec_size(size)(d1 ^ mask(size), d1)


def _rank2(fst: Vector, *rst: VectorLike) -> Array:
    d0, d1 = fst.data
    for i, x in enumerate(rst, start=1):
        x = _expect_vec_size(x, fst.size)
        d0 |= x.data[0] << (fst.size * i)
        d1 |= x.data[1] << (fst.size * i)
    if fst.shape == (1,):
        size = len(rst) + 1
        return _get_vec_size(size)(d0, d1)
    shape = (len(rst) + 1,) + fst.shape
    return _get_array_shape(shape)(d0, d1)


def bits(obj=None) -> Array:
    """Create a shaped Bits object using standard input formats.

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
        obj: Object that can be converted to a Bits instance.

    Returns:
        Shaped ``Bits`` instance.

    Raises:
        TypeError: If input obj is invalid.
    """
    match obj:
        case None | []:
            return _empty
        case 0 | 1 as x:
            return bool2scalar[x]
        case [0 | 1 as fst, *rst]:
            return _bools2vec(fst, *rst)
        case str() as lit:
            return lit2bv(lit)
        case [str() as lit, *rst]:
            x = lit2bv(lit)
            return _rank2(x, *rst)
        case [Scalar() as x, *rst]:
            return _rank2(x, *rst)
        case [Vector() as x, *rst]:
            return _rank2(x, *rst)
        case [*objs]:
            return _stack(*[bits(obj) for obj in objs])
        case _:
            raise TypeError(f"Invalid input: {obj}")


def _stack(*xs: Array) -> Array:
    if len(xs) == 0:
        return _empty
    if len(xs) == 1:
        return xs[0]

    fst, rst = xs[0], xs[1:]

    size = fst.size
    d0, d1 = fst.data
    for x in rst:
        if x.shape != fst.shape:
            s = f"Expected shape {fst.shape}, got {x.shape}"
            raise TypeError(s)
        d0 |= x.data[0] << size
        d1 |= x.data[1] << size
        size += x.size

    # {Empty, Empty, ...} => Empty
    if fst.shape == (0,):
        return _empty

    # {Scalar, Scalar, ...} => Vector[K]
    if fst.shape == (1,):
        size = len(xs)
        return vec_size(size)(d0, d1)

    # {Vector[K], Vector[K], ...} => Array[J,K]
    # {Array[J,K], Array[J,K], ...} => Array[I,J,K]
    shape = (len(xs),) + fst.shape
    return _get_array_shape(shape)(d0, d1)


def stack(*objs: ArrayLike) -> Array:
    """Stack a sequence of Bits w/ same shape into a higher dimensional shape.

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
        Shaped ``Bits`` instance.

    Raises:
        TypeError: If input obj is invalid.
    """
    return _stack(*[expect_array(obj) for obj in objs])


def lit2bv(lit: str) -> Vector:
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
    return vec_size(size)(d0, d1)


def u2bv(n: int, size: int | None = None) -> Vector:
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

    return vec_size(size)(n ^ mask(size), n)


def i2bv(n: int, size: int | None = None) -> Vector:
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

    # Compute required number of bits
    if negative:
        d1 = -n
        min_size = clog2(d1) + 1
    else:
        d1 = n
        min_size = clog2(d1 + 1) + 1
    if size is None:
        size = min_size
    elif size < min_size:
        s = f"Overflow: n = {n} required size ≥ {min_size}, got {size}"
        raise ValueError(s)

    x = vec_size(size)(d1 ^ mask(size), d1)
    if negative:
        s, _ = _neg(x)
        return s
    return x


def _chunk(data: lbv, base: int, size: int) -> lbv:
    m = mask(size)
    return (data[0] >> base) & m, (data[1] >> base) & m


def _sel(x: Array, key: tuple[tuple[int, int], ...]) -> Array:
    assert len(x.shape) == len(key)

    (start, stop), key_r = key[0], key[1:]
    assert 0 <= start <= stop <= x.shape[0]

    # Partial select m:n
    if start != 0 or stop != x.shape[0]:

        if len(key_r) == 0:
            size = stop - start
            d0, d1 = _chunk(x.data, start, size)
            return vec_size(size)(d0, d1)

        if len(key_r) == 1:
            vec = _get_vec_size(x.shape[1])
            xs = []
            for i in range(start, stop):
                d0, d1 = _chunk(x.data, vec.size * i, vec.size)
                xs.append(vec(d0, d1))
            return _stack(*[_sel(x, key_r) for x in xs])

        array = _get_array_shape(x.shape[1:])
        xs = []
        for i in range(start, stop):
            d0, d1 = _chunk(x.data, array.size * i, array.size)
            xs.append(array(d0, d1))
        return _stack(*[_sel(x, key_r) for x in xs])

    # Full select 0:n
    if key_r:
        return _stack(*[_sel(xx, key_r) for xx in x])

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


def _norm_slice(n: int, sl: slice) -> tuple[int, int]:
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
    return start, stop


def _get_sep(indent: str, x: Array) -> str:
    # 2-D Matrix
    if len(x.shape) == 2:
        return ", "
    # 3-D
    if len(x.shape) == 3:
        return ",\n" + indent
    # N-D
    return ",\n\n" + indent


def _array_repr(indent: str, x: Array) -> str:
    # 1-D Vector
    if len(x.shape) == 1:
        return f'"{x}"'
    sep = _get_sep(indent, x)
    f = partial(_array_repr, indent + " ")
    return "[" + sep.join(map(f, x)) + "]"


def _array_str(indent: str, x: Array) -> str:
    # 1-D Vector
    if len(x.shape) == 1:
        return f"{x}"
    sep = _get_sep(indent, x)
    f = partial(_array_str, indent + " ")
    return "[" + sep.join(map(f, x)) + "]"
