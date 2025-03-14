import pytest

from yandex_testing_lesson import is_under_queen_attack


# Тесты на валидацию типов
def test_first_arg_not_string():
    """Test TypeError is raised when first argument is not a string"""
    with pytest.raises(TypeError):
        is_under_queen_attack(123, "e5")


def test_second_arg_not_string():
    """Test TypeError is raised when second argument is not a string"""
    with pytest.raises(TypeError):
        is_under_queen_attack("e5", 123)


# Тесты на валидацию формата координат
def test_first_arg_invalid_length():
    """Test ValueError is raised when first coordinate has invalid length"""
    with pytest.raises(ValueError):
        is_under_queen_attack("abc", "e5")


def test_first_arg_invalid_letter():
    """Test ValueError is raised when first coordinate has invalid letter"""
    with pytest.raises(ValueError):
        is_under_queen_attack("j5", "e5")


def test_first_arg_invalid_number():
    """Test ValueError is raised when first coordinate has invalid number"""
    with pytest.raises(ValueError):
        is_under_queen_attack("e9", "e5")


def test_second_arg_invalid_length():
    """Test ValueError is raised when second coordinate has invalid length"""
    with pytest.raises(ValueError):
        is_under_queen_attack("e5", "abc")


def test_second_arg_invalid_letter():
    """Test ValueError is raised when second coordinate has invalid letter"""
    with pytest.raises(ValueError):
        is_under_queen_attack("e5", "j5")


def test_second_arg_invalid_number():
    """Test ValueError is raised when second coordinate has invalid number"""
    with pytest.raises(ValueError):
        is_under_queen_attack("e5", "e9")


# Тесты на логику атаки ферзя
def test_same_position():
    """Test queen attacks the position it stands on"""
    assert is_under_queen_attack("e5", "e5") is True


def test_horizontal_attack():
    """Test queen attacks horizontally"""
    assert is_under_queen_attack("a5", "e5") is True


def test_vertical_attack():
    """Test queen attacks vertically"""
    assert is_under_queen_attack("e1", "e5") is True


def test_diagonal_attack_1():
    """Test queen attacks diagonally (first diagonal)"""
    assert is_under_queen_attack("c3", "e5") is True


def test_diagonal_attack_2():
    """Test queen attacks diagonally (second diagonal)"""
    assert is_under_queen_attack("g3", "e5") is True


def test_no_attack():
    """Test queen doesn't attack positions that are not on attack lines"""
    assert is_under_queen_attack("b1", "e5") is False
    assert is_under_queen_attack("d2", "e5") is False
