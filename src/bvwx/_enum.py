"""Bits Enum data type."""

from typing import Any

from ._bits import ArrayLike, Vector, cast_data, expect_array_size, vec_size
from ._lbool import parse_lit
from ._util import mask

type Data2Key = dict[tuple[int, int], str]


def _parse_attrs(attrs: dict[str, Any]) -> tuple[dict[str, Any], Data2Key, int]:
    _attrs: dict[str, Any] = {}
    data2key: Data2Key = {}
    size: int | None = None
    xx = (0, 0)
    ww = (-1, -1)

    for key, val in attrs.items():
        if key.startswith("__"):
            _attrs[key] = val
        # NAME = lit
        else:
            if size is None:
                size, data = parse_lit(val)
                dmax = mask(size)
                ww = (dmax, dmax)
            else:
                size_i, data = parse_lit(val)
                if size_i != size:
                    s = f"Expected lit len {size}, got {size_i}"
                    raise ValueError(s)
            if key in ("X", "W"):
                raise ValueError(f"Cannot use reserved name = '{key}'")
            if data in (xx, ww):
                raise ValueError(f"Cannot use reserved value = {val}")
            if data in data2key:
                raise ValueError(f"Duplicate value: {val}")
            data2key[data] = key

    # Empty Enum
    if size is None:
        raise ValueError("Empty Enum is not supported")

    # Add X/W members
    data2key[xx] = "X"
    data2key[ww] = "W"

    return _attrs, data2key, size


def _vcd_var(self) -> str:
    return "string"


class EnumType(type):
    """Enum Metaclass: Create enum base classes."""

    _data2key: Data2Key

    def __new__(
        mcls,
        name: str,
        bases: tuple[()] | tuple[type],
        attrs: dict[str, Any],
    ):
        # Base case for API
        if name == "Enum":
            assert not bases
            return super().__new__(mcls, name, bases, attrs)

        # Do not support multiple inheritance
        assert len(bases) == 1

        _, data2key, size = _parse_attrs(attrs)

        # Get Vector[N] base class
        V = vec_size(size)

        # Create Enum class
        ns: dict[str, Any] = {"__slots__": (), "_data2key": data2key}
        cls = super().__new__(mcls, name, (V,), ns)

        def _cast_data(cls, d0: int, d1: int) -> Vector:
            try:
                return getattr(cls, data2key[(d0, d1)])
            except KeyError:
                return cast_data(cls, d0, d1)

        def _repr(self) -> str:
            try:
                return f"{name}.{data2key[self._data]}"
            except KeyError:
                return f'{name}("{V.__str__(self)}")'

        def _str(self) -> str:
            try:
                return f"{name}.{data2key[self._data]}"
            except KeyError:
                return f"{name}({V.__str__(self)})"

        def _name(self) -> str:
            try:
                return data2key[self._data]
            except KeyError:
                return f"{name}({V.__str__(self)})"

        # Override Array methods
        setattr(cls, "_cast_data", classmethod(_cast_data))
        setattr(cls, "__repr__", _repr)
        setattr(cls, "__str__", _str)
        setattr(cls, "vcd_var", _vcd_var)
        setattr(cls, "vcd_val", _name)

        # Enum.name
        setattr(cls, "name", property(fget=_name))

        return cls

    def __init__(
        cls,
        name: str,
        bases: tuple[()] | tuple[type],
        attrs: dict[str, Any],
    ):
        # Base case for API
        if name == "Enum":
            assert not bases
            return

        assert issubclass(cls, Vector)  # Help type checker

        # Instantiate members
        for (d0, d1), key in cls._data2key.items():
            setattr(cls, key, cast_data(cls, d0, d1))

    def __call__(cls, arg: ArrayLike):
        assert issubclass(cls, Vector)  # Help type checker
        x = expect_array_size(arg, cls.size)
        return cls._cast_data(x._data[0], x._data[1])


class Enum(metaclass=EnumType):
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

    All ``Enums`` have ``X`` and ``W`` attributes defined automatically:

    >>> Color.X == "2bXX"
    True
    >>> Color.W == "2b--"
    True

    To cast a ``Vec`` to an ``Enum``, use the constructor:

    >>> Color("2b00")
    Color.RED

    Values not included in the enumeration are allowed:

    >>> Color("2b11")
    Color("2b11")

    To cast an ``Enum`` to a ``Vec``, use the ``cast`` method:

    >>> from bvwx import Vec, cast
    >>> cast(Vec[2], Color.RED)
    bits("2b00")
    """
