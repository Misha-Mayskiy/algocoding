import pytest

from yandex_testing_lesson import count_chars


def test_normal_string():
    """Test counting characters in a normal string"""
    result = count_chars("hello")
    expected = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    assert result == expected


def test_empty_string():
    """Test counting characters in an empty string"""
    result = count_chars("")
    expected = {}
    assert result == expected


def test_string_with_spaces():
    """Test counting characters in a string with spaces"""
    result = count_chars("hello world")
    expected = {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
    assert result == expected


def test_string_with_special_chars():
    """Test counting characters in a string with special characters"""
    result = count_chars("hello!")
    expected = {'h': 1, 'e': 1, 'l': 2, 'o': 1, '!': 1}
    assert result == expected


def test_string_with_case_sensitivity():
    """Test that the function is case-sensitive"""
    result = count_chars("Hello")
    expected = {'H': 1, 'e': 1, 'l': 2, 'o': 1}
    assert result == expected


def test_non_string_input():
    """Test that TypeError is raised for non-string input"""
    with pytest.raises(TypeError):
        count_chars(123)


def test_non_string_iterable_input():
    """Test that TypeError is raised for non-string iterable input"""
    with pytest.raises(TypeError):
        count_chars([1, 2, 3])
