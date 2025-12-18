"""Bits Tuple data type."""

from ._bits import Array, ArrayLike, Vector, expect_array, vec_size
from ._util import mask


def Tuple(*objs: ArrayLike):
    # [(offset, type), ...]
    fields: list[tuple[int, type[Array]]] = []

    offset = 0
    d0, d1 = 0, 0
    for obj in objs:
        x = expect_array(obj)
        fields.append((offset, x.__class__))
        d0 |= x.data[0] << offset
        d1 |= x.data[1] << offset
        offset += x.size

    # Get Vector[N] base class
    V = vec_size(offset)

    # Create Tuple class
    name = "Tuple[" + ", ".join(ft.__name__ for _, ft in fields) + "]"
    tuple_ = type(name, (V,), {"__slots__": ()})

    # Override Tuple.__getitem__ method
    def _getitem(self: Vector, key: int):
        offset, ft = fields[key]
        m = mask(ft.size)
        d0 = (self._data[0] >> offset) & m  # pyright: ignore[reportPrivateUsage]
        d1 = (self._data[1] >> offset) & m  # pyright: ignore[reportPrivateUsage]
        return ft.cast_data(d0, d1)

    tuple_.__getitem__ = _getitem  # pyright: ignore[reportAttributeAccessIssue]

    # Return Tuple[...] instance
    return tuple_.cast_data(d0, d1)
