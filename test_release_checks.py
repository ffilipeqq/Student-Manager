import unittest

from release_checks import is_valid_name

class NameTests(unittest.TestCase):
    def test_valid_name(self):
        self.assertTrue(is_valid_name("Alex"))

    def test_blank_name(self):
        self.assertFalse(is_valid_name(" "))

    def test_short_name(self):
        self.assertFalse(is_valid_name("A"))

    def test_long_name(self):
        self.assertFalse(is_valid_name("A" * 51))
        
