"""Bits Tuple data type."""

from ._bits import Array, ArrayLike, Vector, expect_array, vec_size
from ._util import mask


def Tuple(*args: ArrayLike) -> Vector:
    # [(offset, type), ...]
    fields: list[tuple[int, type[Array]]] = []

    field_offset = 0
    d0, d1 = 0, 0
    for arg in args:
        x = expect_array(arg)
        fields.append((field_offset, x.__class__))
        d0 |= x.data[0] << field_offset
        d1 |= x.data[1] << field_offset
        field_offset += x.size

    # Get Vector[N] base class
    V = vec_size(field_offset)

    # Create Tuple class
    name = "Tuple[" + ", ".join(ft.__name__ for _, ft in fields) + "]"
    tuple_ = type(name, (V,), {"__slots__": ()})

    # Override Tuple.__getitem__ method
    def _getitem(self: Vector, key: int):
        fo, ft = fields[key]
        m = mask(ft.size)
        d0 = (self._data[0] >> fo) & m  # pyright: ignore[reportPrivateUsage]
        d1 = (self._data[1] >> fo) & m  # pyright: ignore[reportPrivateUsage]
        return ft.cast_data(d0, d1)

    setattr(tuple_, "__getitem__", _getitem)

    # Return Tuple[...] instance
    return tuple_.cast_data(d0, d1)
