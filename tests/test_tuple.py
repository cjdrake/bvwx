"""Test bvwx Tuple."""

import pytest

from bvwx import Tuple, bits


def test_simple():
    t = Tuple("16hface", "16hfeed", "16hbeef", "16hdead")

    assert type(t).__name__ == "Tuple[Vector[16], Vector[16], Vector[16], Vector[16]]"

    assert t == bits("64hdead_beef_feed_face")

    assert t[-1] == bits("16hdead")
    assert t[-2] == bits("16hbeef")
    assert t[-3] == bits("16hfeed")
    assert t[-4] == bits("16hface")

    with pytest.raises(IndexError):
        t[-5]

    with pytest.raises(IndexError):
        t[4]

    assert t[3] == bits("16hdead")
    assert t[2] == bits("16hbeef")
    assert t[1] == bits("16hfeed")
    assert t[0] == bits("16hface")
