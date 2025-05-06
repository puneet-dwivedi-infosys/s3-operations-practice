import pytest
from src.utils.utils import is_prime

@pytest.mark.parametrize("n, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (7, True),
])
def test_is_prime(n, expected):
    assert is_prime(n) == expected