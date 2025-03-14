import pytest

from yandex_testing_lesson import reverse


def test_empty_string():
    """Test reverse of empty string"""
    assert reverse("") == ""


def test_single_char():
    """Test reverse of single character"""
    assert reverse("a") == "a"


def test_palindrome():
    """Test reverse of palindrome"""
    assert reverse("шалаш") == "шалаш"


def test_regular_string():
    """Test reverse of regular string"""
    assert reverse("привет") == "тевирп"


def test_non_iterable():
    """Test non-iterable input"""
    with pytest.raises(TypeError):
        reverse(42)


def test_iterable_non_string():
    """Test iterable non-string input"""
    with pytest.raises(TypeError):
        reverse([1, 2, 3])
