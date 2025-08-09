"""Bits Union data type."""

from functools import partial
from typing import Any

from ._bits import Bits, BitsLike, Composite, expect_bits
from ._util import mask


class _UnionMeta(type):
    """Union Metaclass: Create union base classes."""

    def __new__(mcs, name: str, bases: tuple[type], attrs: dict[str, Any]):
        # Base case for API
        if name == "Union":
            return super().__new__(mcs, name, bases, attrs)

        # TODO(cjdrake): Support multiple inheritance?
        assert len(bases) == 1

        # Get field_name: field_type items
        try:
            annotations: dict[str, type[Bits]] = attrs["__annotations__"]
        except KeyError as e:
            raise ValueError("Empty Union is not supported") from e

        fields = list(annotations.items())

        # Create Union class
        size = max(field_type.size for _, field_type in fields)
        union = super().__new__(mcs, name, bases, {"size": size})

        # Help the type checker
        assert issubclass(union, Composite)

        # Override Bits.__init__ method
        def _init(self: Union, arg: BitsLike):
            x = expect_bits(arg)
            ts = {ft for _, ft in fields}
            if not isinstance(x, tuple(ts)):
                s = ", ".join(t.__name__ for t in ts)
                s = f"Expected arg to be {{{s}}}, or str literal"
                raise TypeError(s)
            self._data = x.data  # pyright: ignore[reportPrivateUsage]

        setattr(union, "__init__", _init)

        # Override Bits.__str__ method
        def _str(self: Union) -> str:
            parts = [f"{name}("]
            for fn, _ in fields:
                x = getattr(self, fn)
                s = "\n    ".join(str(x).splitlines())
                parts.append(f"    {fn}={s},")
            parts.append(")")
            return "\n".join(parts)

        setattr(union, "__str__", _str)

        # Override Bits.__repr__ method
        def _repr(self: Union) -> str:
            parts = [f"{name}("]
            for fn, _ in fields:
                x = getattr(self, fn)
                r = "\n    ".join(repr(x).splitlines())
                parts.append(f"    {fn}={r},")
            parts.append(")")
            return "\n".join(parts)

        setattr(union, "__repr__", _repr)

        # Create Union fields
        def _fget(ft: type[Bits], self: Union):
            m = mask(ft.size)
            d0 = self._data[0] & m  # pyright: ignore[reportPrivateUsage]
            d1 = self._data[1] & m  # pyright: ignore[reportPrivateUsage]
            return ft.cast_data(d0, d1)

        for fn, ft in fields:
            setattr(union, fn, property(fget=partial(_fget, ft)))

        return union


class Union(Composite, metaclass=_UnionMeta):
    """User defined union data type.

    Compose a type from the union of other types.

    Extend from ``Union`` to define a union:

    >>> from bvwx import Vec
    >>> class Response(Union):
    ...     error: Vec[4]
    ...     data: Vec[8]

    Use the new type's constructor to create ``Union`` instances:

    >>> rsp = Response("8h0f")

    Access individual fields using attributes:

    >>> rsp.error
    bits("4b1111")
    >>> rsp.data
    bits("8b0000_1111")

    ``Unions`` have a ``size``, but no ``shape``.
    They do **NOT** implement a ``__len__`` method.

    >>> Response.size
    8

    ``Union`` slicing behaves like a ``Vector``:

    >>> rsp[3:5]
    bits("2b01")
    """
