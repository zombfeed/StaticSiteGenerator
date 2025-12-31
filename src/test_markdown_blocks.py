from typing import MutableMapping
import unittest
from markdown_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


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


class TestBlockToBlockType(unittest.TestCase):
    def test_block_is_paragraph(self):
        block = "this is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_is_heading(self):
        block = "# this is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_is_not_heading(self):
        block = "#this is not a heading"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_is_code(self):
        block = "```\nthis is a code block\n```"
        multiline_block = "```\nthis is a code block\nwith multiple lines\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(block_to_block_type(multiline_block), BlockType.CODE)

    def test_block_is_not_code(self):
        block = "```this is not code"
        multiline_block = "```\nthis is not code\nbecause it doesnt end in backquotes"
        multiline_block2 = (
            "this is not code\nbecause it doesnt start with backquotes\n```"
        )
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(multiline_block), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(multiline_block2), BlockType.CODE)

    def test_block_is_quote(self):
        block = ">this is a quote"
        multiline_block = ">this is a quote\n> this is also a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(multiline_block), BlockType.QUOTE)

    def test_block_is_not_quote(self):
        block = "this is not a quote"
        multiline_block = ">this is not a block\nbecause not every line starts with a >"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(multiline_block), BlockType.QUOTE)

    def test_block_is_unordered(self):
        block = "- this is unordered"
        multiline_block = "- this is unordered\n- this is the second line"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(multiline_block), BlockType.UNORDERED_LIST)

    def test_block_is_not_unordered(self):
        block = "-this is not unordered"
        multiline_block = (
            "- this is not unordered\n-because not every line starts with '- '"
        )
        multiline_block2 = (
            "-this is not unordered\n- because not every line starts with '- '"
        )
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        self.assertNotEqual(
            block_to_block_type(multiline_block), BlockType.UNORDERED_LIST
        )
        self.assertNotEqual(
            block_to_block_type(multiline_block2), BlockType.UNORDERED_LIST
        )

    def test_block_is_ordered(self):
        block = "1. This is ordered"
        multiline_block = (
            "1. This is ordered\n2. This is the second\n3. This is the third"
        )
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(multiline_block), BlockType.ORDERED_LIST)

    def test_block_is_not_ordered(self):
        block = "1.This is not ordered"
        block2 = "2. This is not ordered"
        multiline_block = "1. This is not ordered\n2.This is not ordered"
        mutliline_block2 = "1. This is not ordered\n3. This is not ordered"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(block2), BlockType.ORDERED_LIST)
        self.assertNotEqual(
            block_to_block_type(multiline_block), BlockType.ORDERED_LIST
        )
        self.assertNotEqual(
            block_to_block_type(mutliline_block2), BlockType.ORDERED_LIST
        )


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html(self):
        md = """
## this is a heading

### this is another heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

>here is a quote by some guy
>he said this thing

- this is an unordered list item
- this is also a ulist item

1. this is an ordered list item
2. this is another olist item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>this is a heading</h2><h3>this is another heading</h3><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><blockquote>here is a quote by some guy he said this thing</blockquote><ul><li>this is an unordered list item</li><li>this is also a ulist item</li></ul><ol><li>this is an ordered list item</li><li>this is another olist item</li></ol></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
>This is a quote block that
>This is another part of the block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block that This is another part of the block</blockquote></div>",
        )

    def test_unorderedlist(self):
        md = """
- this is an unordered list
- this is another item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is an unordered list</li><li>this is another item</li></ul></div>",
        )

    def test_orderedlist(self):
        md = """
1. this is an ordered list
2. this is another item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is an ordered list</li><li>this is another item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
