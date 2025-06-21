"""Bits Enum data type."""

from typing import Any

from ._bits import Bits, BitsLike, Vector, expect_bits_size, vec_size
from ._lbool import parse_lit
from ._util import mask


class _EnumMeta(type):
    """Enum Metaclass: Create enum base classes."""

    def __new__(mcs, name: str, bases: tuple[()] | tuple[type], attrs: dict[str, Any]):
        # Base case for API
        if name == "Enum":
            assert not bases
            return super().__new__(mcs, name, bases, attrs)

        # TODO(cjdrake): Support multiple inheritance?
        assert len(bases) == 1

        data2key, vec, enum = mcs.parse_attrs(name, bases, attrs)

        # Instantiate members
        for (d0, d1), key in data2key.items():
            setattr(enum, key, enum._cast_data(d0, d1))

        # Override Vector._cast_data method
        def _cast_data(cls, d0: int, d1: int) -> Bits:
            data = (d0, d1)
            try:
                obj = getattr(cls, data2key[data])
            except KeyError:
                obj = object.__new__(cls)
                obj._data = data
            return obj

        enum._cast_data = classmethod(_cast_data)

        # Override Vector.__new__ method
        def _new(cls, arg: BitsLike):
            x = expect_bits_size(arg, cls.size)
            return cls.cast(x)

        enum.__new__ = _new

        # Override Vector.__repr__ method
        def _repr(self) -> str:
            try:
                return f"{name}.{data2key[self._data]}"
            except KeyError:
                return f'{name}("{vec.__str__(self)}")'

        enum.__repr__ = _repr

        # Override Vector.__str__ method
        def _str(self) -> str:
            try:
                return f"{name}.{data2key[self._data]}"
            except KeyError:
                return f"{name}({vec.__str__(self)})"

        enum.__str__ = _str

        # Create name property
        def _name(self) -> str:
            try:
                return data2key[self._data]
            except KeyError:
                return f"{name}({vec.__str__(self)})"

        enum.name = property(fget=_name)

        # Override VCD methods
        enum.vcd_var = lambda _: "string"
        enum.vcd_val = _name

        return enum

    @classmethod
    def parse_attrs(
        mcs, name: str, bases: tuple[type], attrs: dict[str, Any]
    ) -> tuple[dict[tuple[int, int], str], type[Vector], type[Vector]]:
        _attrs: dict[str, Any] = {}
        data2key: dict[tuple[int, int], str] = {}
        size: int | None = None

        for key, val in attrs.items():
            if key.startswith("__"):
                _attrs[key] = val
            # NAME = lit
            else:
                if size is None:
                    size, data = parse_lit(val)
                else:
                    size_i, data = parse_lit(val)
                    if size_i != size:
                        s = f"Expected lit len {size}, got {size_i}"
                        raise ValueError(s)
                if key in ("X", "DC"):
                    raise ValueError(f"Cannot use reserved name = '{key}'")
                dmax = mask(size)
                if data in ((0, 0), (dmax, dmax)):
                    raise ValueError(f"Cannot use reserved value = {val}")
                if data in data2key:
                    raise ValueError(f"Duplicate value: {val}")
                data2key[data] = key

        # Empty Enum
        if size is None:
            raise ValueError("Empty Enum is not supported")

        # Add X/DC members
        data2key[(0, 0)] = "X"
        dmax = mask(size)
        data2key[(dmax, dmax)] = "DC"

        vec = vec_size(size)

        # Create Enum class
        enum = super().__new__(mcs, name, bases + (vec,), _attrs)

        return data2key, vec, enum


class Enum(metaclass=_EnumMeta):
    """User-defined enumerated data type.

    Define a type from a collection of unique constants.

    Extend from ``Enum`` to define an enumeration:

    >>> from bvwx import Enum
    >>> class Color(Enum):
    ...     RED = "2b00"
    ...     GREEN = "2b01"
    ...     BLUE = "2b10"

    ``Enums`` behave like ``Vectors``,
    but they have an extra ``name`` attribute:

    >>> len(Color.RED)
    2
    >>> Color.RED[0]
    bits("1b0")
    >>> Color.RED == "2b00"
    True
    >>> Color.RED.name
    'RED'

    All ``Enums`` have ``X`` and ``DC`` attributes defined automatically:

    >>> Color.X == "2bXX"
    True
    >>> Color.DC == "2b--"
    True

    To cast a ``Vec`` to an ``Enum``, use the constructor:

    >>> Color("2b00")
    Color.RED

    Values not included in the enumeration are allowed:

    >>> Color("2b11")
    Color("2b11")

    To cast an ``Enum`` to a ``Vec``, use the ``cast`` method:

    >>> from bvwx import Vec
    >>> Vec[2].cast(Color.RED)
    bits("2b00")
    """
