import unittest

from yandex_testing_lesson import reverse


class TestReverse(unittest.TestCase):

    def test_empty_string(self):
        """Test reverse of empty string"""
        self.assertEqual(reverse(""), "")

    def test_single_char(self):
        """Test reverse of single character"""
        self.assertEqual(reverse("a"), "a")

    def test_palindrome(self):
        """Test reverse of palindrome"""
        self.assertEqual(reverse("шалаш"), "шалаш")

    def test_regular_string(self):
        """Test reverse of regular string"""
        self.assertEqual(reverse("привет"), "тевирп")

    def test_non_iterable(self):
        """Test non-iterable input"""
        with self.assertRaises(TypeError):
            reverse(42)

    def test_iterable_non_string(self):
        """Test iterable non-string input"""
        with self.assertRaises(TypeError):
            reverse([1, 2, 3])


if __name__ == '__main__':
    unittest.main()
