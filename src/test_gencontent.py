import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        title = extract_title("# this is a title")
        self.assertEqual(title, "this is a title")

    def test_eq_multi(self):
        title = extract_title(
            """
# This is the first title

# This is the second title

# This is the third title
"""
        )
        self.assertEqual(title, "This is the first title")

    def test_eq_long(self):
        title = extract_title(
            """
# this is the title

this
is

- extra
- text
"""
        )
        self.assertEqual(title, "this is the title")

    def test_none(self):
        with self.assertRaises(Exception):
            extract_title("no title")


if __name__ == "__main__":
    unittest.main()
