import pytest

from yandex_testing_lesson import is_under_queen_attack


@pytest.mark.parametrize("position, queen_position, expected", [
    # Same position
    ("a1", "a1", True),
    ("h8", "h8", True),
    # Horizontal
    ("a1", "a8", True),
    ("h3", "a3", True),
    # Vertical
    ("b1", "b7", True),
    ("c5", "c2", True),
    # Diagonal
    ("b3", "d5", True),
    ("d4", "a1", True),
    ("d4", "g7", True),
    ("e5", "h8", True),
    ("a8", "h1", True),
    # Not under attack
    ("a1", "b3", False),
    ("d4", "e6", False),
    ("c2", "e5", False),
    ("h8", "g6", False),
])
def test_queen_attack_cases(position, queen_position, expected):
    assert is_under_queen_attack(position, queen_position) == expected


@pytest.mark.parametrize("position, queen_position, error", [
    # TypeError cases
    (123, "a1", TypeError),
    ("a1", 456, TypeError),
    (None, "a1", TypeError),
    ("a1", ["h8"], TypeError),
    # ValueError cases for position
    ("i1", "a1", ValueError),
    ("a9", "a1", ValueError),
    ("a0", "a1", ValueError),
    ("k5", "a1", ValueError),
    ("A1", "a1", ValueError),
    ("a", "a1", ValueError),
    ("a12", "a1", ValueError),
    ("a1 ", "a1", ValueError),
    # ValueError cases for queen_position
    ("a1", "i1", ValueError),
    ("a1", "a9", ValueError),
    ("a1", "a0", ValueError),
    ("a1", "k5", ValueError),
    ("a1", "A1", ValueError),
    ("a1", "a", ValueError),
    ("a1", "a12", ValueError),
    ("a1", "a1 ", ValueError),
])
def test_error_cases(position, queen_position, error):
    with pytest.raises(error):
        is_under_queen_attack(position, queen_position)


def test_error_order():
    # First argument is invalid type
    with pytest.raises(TypeError):
        is_under_queen_attack(123, "a9")
    # First argument is invalid value, second is invalid type
    with pytest.raises(ValueError):
        is_under_queen_attack("j5", 456)
    # Both arguments are invalid, but first fails first
    with pytest.raises(ValueError):
        is_under_queen_attack("a9", 456)
