import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextType, TextNode
import textnode


class TestTextToTextNode(unittest.TestCase):
    def test_multiple_texttypes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_node,
        )

    def test_single_texttypes(self):
        text = "**THIS** is **BOLD** and **MORE** bold"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("THIS", TextType.BOLD),
                TextNode(" is ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("MORE", TextType.BOLD),
                TextNode(" bold", TextType.TEXT),
            ],
            new_node,
        )

    def test_nested_texttypes(self):
        text = "**_THIS SHOULD BE ITALIC_** and not bold"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("_THIS SHOULD BE ITALIC_", TextType.BOLD),
                TextNode(" and not bold", TextType.TEXT),
            ],
            new_node,
        )


if __name__ == "__main__":
    unittest.main()
