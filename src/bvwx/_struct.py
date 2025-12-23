"""Bits Struct data type."""

from functools import partial
from typing import Any

from ._bits import Array, ArrayLike, Bits, Vector, expect_array_size, vec_size
from ._util import mask


def _struct_init_source(fields: list[tuple[str, int, type]]) -> str:
    """Return source code for Struct __init__ method w/ fields."""
    lines: list[str] = []
    s = ", ".join(f"{fn}=None" for fn, _, _ in fields)
    lines.append(f"def init(self, {s}):\n")
    s = ", ".join(fn for fn, _, _ in fields)
    lines.append(f"    _init_body(self, {s})\n")
    return "".join(lines)


class _StructMeta(type):
    """Struct Metaclass: Create struct base classes."""

    def __new__(mcs, name: str, bases: tuple[type], attrs: dict[str, Any]):
        # Base case for API
        if name == "Struct":
            attrs["__slots__"] = ()
            return super().__new__(mcs, name, bases, attrs)

        # Do not support multiple inheritance
        assert len(bases) == 1

        # Get field_name: field_type items
        try:
            annotations: dict[str, type[Array]] = attrs["__annotations__"]
        except KeyError as e:
            raise ValueError("Empty Struct is not supported") from e

        # [(name, offset, type), ...]
        fields: list[tuple[str, int, type[Array]]] = []

        # Add struct member base/size attributes
        field_offset = 0
        for field_name, field_type in annotations.items():
            fields.append((field_name, field_offset, field_type))
            field_offset += field_type.size

        # Get Vector[N] base class
        V = vec_size(field_offset)

        # Create Struct class
        struct = super().__new__(mcs, name, bases + (V,), {"__slots__": ()})

        # Override Array.__init__ method
        def _init_body(obj: Vector, *args: ArrayLike | None):
            d0, d1 = 0, 0
            for arg, (_, fo, ft) in zip(args, fields):
                if arg is not None:
                    x = expect_array_size(arg, ft.size)
                    d0 |= x.data[0] << fo
                    d1 |= x.data[1] << fo
            Bits.__init__(obj, d0, d1)

        source = _struct_init_source(fields)
        globals_ = {"_init_body": _init_body}
        locals_: dict[str, Any] = {}
        exec(source, globals_, locals_)
        struct.__init__ = locals_["init"]

        # Override Array.__repr__ method
        def _repr(self: Vector) -> str:
            parts = [f"{name}("]
            for fn, _, _ in fields:
                x = getattr(self, fn)
                r = "\n    ".join(repr(x).splitlines())
                parts.append(f"    {fn}={r},")
            parts.append(")")
            return "\n".join(parts)

        setattr(struct, "__repr__", _repr)

        # Override Array.__str__ method
        def _str(self: Vector) -> str:
            parts = [f"{name}("]
            for fn, _, _ in fields:
                x = getattr(self, fn)
                s = "\n    ".join(str(x).splitlines())
                parts.append(f"    {fn}={s},")
            parts.append(")")
            return "\n".join(parts)

        setattr(struct, "__str__", _str)

        # Create Struct fields
        def _fget(fo: int, ft: type[Array], self: Vector):
            m = mask(ft.size)
            d0 = (self._data[0] >> fo) & m  # pyright: ignore[reportPrivateUsage]
            d1 = (self._data[1] >> fo) & m  # pyright: ignore[reportPrivateUsage]
            return ft.cast_data(d0, d1)

        for fn, fo, ft in fields:
            setattr(struct, fn, property(fget=partial(_fget, fo, ft)))

        return struct


class Struct(metaclass=_StructMeta):
    """User defined struct data type.

    Compose a type from a sequence of other types.

    Extend from ``Struct`` to define a struct:

    >>> from bvwx import Vec
    >>> class Pixel(Struct):
    ...     red: Vec[8]
    ...     green: Vec[8]
    ...     blue: Vec[8]

    Use the new type's constructor to create ``Struct`` instances:

    >>> maize = Pixel(red="8hff", green="8hcb", blue="8h05")

    Access individual fields using attributes:

    >>> maize.red
    bits("8b1111_1111")
    >>> maize.green
    bits("8b1100_1011")

    ``Structs`` have a ``size``, but no ``shape``.

    >>> Pixel.size
    24

    ``Struct`` slicing behaves like a ``Vector``:

    >>> maize[8:16] == maize.green
    True
    """
