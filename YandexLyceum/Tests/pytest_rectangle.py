import pytest

from yandex_testing_lesson import Rectangle


# Тесты на создание прямоугольника с корректными параметрами
def test_rectangle_creation():
    rect = Rectangle(5, 10)
    assert isinstance(rect, Rectangle)


# Тесты на выбрасывание TypeError при некорректном типе данных
def test_width_type_error():
    with pytest.raises(TypeError):
        Rectangle("5", 10)


def test_height_type_error():
    with pytest.raises(TypeError):
        Rectangle(5, "10")


def test_both_params_type_error():
    with pytest.raises(TypeError):
        Rectangle("width", "height")


# Тесты на выбрасывание ValueError при отрицательных значениях
def test_negative_width():
    with pytest.raises(ValueError):
        Rectangle(-5, 10)


def test_negative_height():
    with pytest.raises(ValueError):
        Rectangle(5, -10)


def test_both_negative():
    with pytest.raises(ValueError):
        Rectangle(-5, -10)


# Тесты на вычисление площади
def test_area_calculation():
    rect = Rectangle(5, 10)
    assert rect.get_area() == 50


def test_zero_area():
    rect = Rectangle(0, 10)
    assert rect.get_area() == 0


# Тесты на вычисление периметра
def test_perimeter_calculation():
    rect = Rectangle(5, 10)
    assert rect.get_perimeter() == 30


def test_perimeter_with_zero():
    rect = Rectangle(0, 5)
    assert rect.get_perimeter() == 10


# Тесты с дробными значениями
def test_float_values():
    rect = Rectangle(5.5, 10.5)
    assert rect.get_area() == 5.5 * 10.5
    assert rect.get_perimeter() == 2 * (5.5 + 10.5)


# Тест случая квадрата (равные стороны)
def test_square():
    rect = Rectangle(7, 7)
    assert rect.get_area() == 49
    assert rect.get_perimeter() == 28
