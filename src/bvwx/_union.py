"""Bits Union data type."""

import sys
from functools import partial
from typing import Any

if sys.version_info >= (3, 14):
    from annotationlib import Format, get_annotate_from_class_namespace

from ._bits import Array, ArrayLike, expect_array, vec_size
from ._util import mask


def _get_annotations(attrs: dict[str, Any]) -> dict[str, Any]:
    if sys.version_info >= (3, 14):
        f = get_annotate_from_class_namespace(attrs)
        if f is not None:
            return f(Format.VALUE)
        else:
            raise ValueError("Empty Union is not supported")
    try:
        return attrs["__annotations__"]
    except KeyError as e:
        raise ValueError("Empty Union is not supported") from e


class UnionType(type):
    """Union Metaclass: Create union base classes."""

    def __new__(
        mcls,
        name: str,
        bases: tuple[()] | tuple[type],
        attrs: dict[str, Any],
    ):
        # Base case for API
        if name == "Union":
            assert not bases
            return super().__new__(mcls, name, bases, attrs)

        # Do not support multiple inheritance
        assert len(bases) == 1

        # Get field_name: field_type items
        _annotations = _get_annotations(attrs)

        # Fix / Check annotation types
        annotations: dict[str, type[Array]] = {}
        for k, ft in _annotations.items():
            if not issubclass(ft, Array):
                s = f"Expected annotation type Array, got {ft.__name__}"
                raise TypeError(s)
            annotations[k] = ft

        # [(name, type), ...]
        fields = list(annotations.items())

        # Get Vector[N] base class
        size = max(field_type.size for _, field_type in fields)
        V = vec_size(size)

        # Create Union class
        ns: dict[str, Any] = {"__slots__": ()}
        cls = super().__new__(mcls, name, (V,), ns)

        def _init(self, arg: ArrayLike):
            x = expect_array(arg)
            ts = {ft for _, ft in fields}
            if not isinstance(x, tuple(ts)):
                s = ", ".join(t.__name__ for t in ts)
                s = f"Expected arg to be {{{s}}}, or str literal"
                raise TypeError(s)
            self._data = x._data

        def _repr(self) -> str:
            parts = [f"{name}("]
            for fn, _ in fields:
                x = getattr(self, fn)
                r = "\n    ".join(repr(x).splitlines())
                parts.append(f"    {fn}={r},")
            parts.append(")")
            return "\n".join(parts)

        def _str(self) -> str:
            parts = [f"{name}("]
            for fn, _ in fields:
                x = getattr(self, fn)
                s = "\n    ".join(str(x).splitlines())
                parts.append(f"    {fn}={s},")
            parts.append(")")
            return "\n".join(parts)

        def _fget(ft: type[Array], self):
            m = mask(ft.size)
            d0 = self._data[0] & m
            d1 = self._data[1] & m
            return ft._cast_data(d0, d1)

        # Override Array methods
        setattr(cls, "__init__", _init)
        setattr(cls, "__repr__", _repr)
        setattr(cls, "__str__", _str)

        # Create Union fields
        for fn, ft in fields:
            setattr(cls, fn, property(fget=partial(_fget, ft)))

        return cls


class Union(metaclass=UnionType):
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

    >>> Response.size
    8

    ``Union`` slicing behaves like a ``Vector``:

    >>> rsp[3:5]
    bits("2b01")
    """
