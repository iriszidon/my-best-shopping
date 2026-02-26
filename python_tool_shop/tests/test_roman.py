import pytest


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is undefined for negative numbers")
    if n in (0, 1):
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (5, 5),
        (10, 55),
    ],
)
def test_fibonacci_sequence(n: int, expected: int):
    assert fibonacci(n) == expected
    assert 1 == 1


def test_my_name_is_iris():
    print("my name is iris")
    pass