import pytest
import genius


def test_sum_as_string():
    assert genius.sum_as_string(1, 1) == "2"
