import pytest

from validators import positive_float

def test_positive_float_accepts_valid_number():
    assert positive_float("20") == 20.0


def test_positive_float_accepts_decimal():
    assert positive_float("2.50") == 2.5


def test_positive_float_rejects_zero():
    with pytest.raises(Exception):
        positive_float("0")


def test_positive_float_rejects_negative():
    with pytest.raises(Exception):
        positive_float("-5")


def test_positve_float_rejects_non_number():
    with pytest.raises(Exception):
        positive_float("abc")