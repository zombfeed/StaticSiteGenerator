import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkddownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_line_markdown(self):
        md = """THIS IS A BOLDED PARAGRAPH"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["THIS IS A BOLDED PARAGRAPH"])

    def test_many_white_spaces(self):
        md = """
            THIS HAS WHITESPACE
this doesn't
-this does        
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, ["THIS HAS WHITESPACE\nthis doesn't\n-this does"])


if __name__ == "__main__":
    unittest.main()
