"""Bits Struct data type."""

import sys
from functools import partial
from types import GenericAlias
from typing import Any

if sys.version_info >= (3, 14):
    from annotationlib import Format, get_annotate_from_class_namespace

from ._bits import Array, ArrayLike, expect_array_size, vec

type Field = tuple[str, int, type[Array]]


def _get_annotations(attrs: dict[str, Any]) -> dict[str, Any]:
    if sys.version_info >= (3, 14):
        f = get_annotate_from_class_namespace(attrs)
        if f is not None:
            return f(Format.VALUE)
        raise ValueError("Empty Struct is not supported")
    try:
        return attrs["__annotations__"]
    except KeyError as e:
        raise ValueError("Empty Struct is not supported") from e


def _struct_init_source(fields: list[Field]) -> str:
    """Return source code for Struct __init__ method w/ fields."""
    lines: list[str] = []
    s = ", ".join(f"{fn}=None" for fn, _, _ in fields)
    lines.append(f"def init(self, {s}):\n")
    s = ", ".join(fn for fn, _, _ in fields)
    lines.append(f"    _init_body(self, {s})\n")
    return "".join(lines)


class StructType(type):
    """Struct Metaclass: Create struct base classes."""

    def __new__(
        mcls,
        name: str,
        bases: tuple[()] | tuple[type],
        attrs: dict[str, Any],
    ):
        # Base case for API
        if name == "Struct":
            assert not bases
            return super().__new__(mcls, name, bases, attrs)

        # Do not support multiple inheritance
        assert len(bases) == 1

        # Get field_name: field_type items
        _annotations = _get_annotations(attrs)

        # Fix / Check annotation types
        annotations: dict[str, type[Array]] = {}
        for fn, v in _annotations.items():
            ft: type[Array] = v.__origin__ if isinstance(v, GenericAlias) else v
            if not issubclass(ft, Array):
                s = f"Field {fn} expected type Array, got {ft.__name__}"
                raise TypeError(s)
            annotations[fn] = ft

        # [(name, offset, type), ...]
        fields: list[Field] = []

        # Add struct member base/size attributes
        field_offset = 0
        for field_name, field_type in annotations.items():
            fields.append((field_name, field_offset, field_type))
            field_offset += field_type.size

        # Get Vector[N] base class
        V = vec(field_offset)

        # Create Struct class
        ns: dict[str, Any] = {"__slots__": ()}
        cls = super().__new__(mcls, name, (V,), ns)

        def _init_body(obj: Array, *args: ArrayLike | None):
            d0, d1 = 0, 0
            for arg, (_, fo, ft) in zip(args, fields):
                if arg is not None:
                    x = expect_array_size(arg, ft.size)
                    d0 |= x._data[0] << fo
                    d1 |= x._data[1] << fo
            obj._data = (d0, d1)

        source = _struct_init_source(fields)
        globals_: dict[str, Any] = {"_init_body": _init_body}
        locals_: dict[str, Any] = {}
        exec(source, globals_, locals_)

        def _repr(self) -> str:
            parts = [f"{name}("]
            for fn, _, _ in fields:
                x = getattr(self, fn)
                r = "\n    ".join(repr(x).splitlines())
                parts.append(f"    {fn}={r},")
            parts.append(")")
            return "\n".join(parts)

        def _str(self) -> str:
            parts = [f"{name}("]
            for fn, _, _ in fields:
                x = getattr(self, fn)
                s = "\n    ".join(str(x).splitlines())
                parts.append(f"    {fn}={s},")
            parts.append(")")
            return "\n".join(parts)

        def _fget(fo: int, ft: type[Array], self):
            d0 = (self._data[0] >> fo) & ft._dmax
            d1 = (self._data[1] >> fo) & ft._dmax
            return ft._cast_data(d0, d1)

        # Override Array methods
        setattr(cls, "__init__", locals_["init"])
        setattr(cls, "__repr__", _repr)
        setattr(cls, "__str__", _str)

        # Create Struct fields
        for fn, fo, ft in fields:
            if hasattr(cls, fn):
                raise ValueError(f"Cannot use reserved field name: {fn}")
            setattr(cls, fn, property(fget=partial(_fget, fo, ft)))

        return cls


class Struct(metaclass=StructType):
    """User defined struct data type.

    Compose a type from a sequence of other types.

    Extend from ``Struct`` to define a struct:

    >>> from bvwx import Array
    >>> class Pixel(Struct):
    ...     red: Array[8]
    ...     green: Array[8]
    ...     blue: Array[8]

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
