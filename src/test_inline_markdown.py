import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
)

from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_types(self):
        bold_node = TextNode("This is text with a **bold** word", TextType.TEXT)
        italic_node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        code_node = TextNode("This is text with a `code block` word", TextType.TEXT)

        new_bold_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        new_italic_nodes = split_nodes_delimiter([italic_node], "_", TextType.ITALIC)
        new_code_nodes = split_nodes_delimiter([code_node], "`", TextType.CODE)

        self.assertEqual(
            new_bold_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_italic_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_code_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_not_text_type(self):
        bold_node = TextNode("Bold", TextType.BOLD)
        italic_node = TextNode("Italic", TextType.ITALIC)
        code_node = TextNode("code block", TextType.CODE)

        new_bold_node = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        new_italic_node = split_nodes_delimiter([italic_node], "_", TextType.ITALIC)
        new_code_node = split_nodes_delimiter([code_node], "`", TextType.CODE)

        self.assertEqual(new_bold_node, [bold_node])
        self.assertEqual(new_italic_node, [italic_node])
        self.assertEqual(new_code_node, [code_node])

    def test_no_matching_delimiters(self):
        with self.assertRaises(Exception):
            node = TextNode(
                "This is a text with no **matching end delimiter", TextType.TEXT
            )
            split_nodes_delimiter([node], "**", TextType.BOLD)

        with self.assertRaises(Exception):
            node = TextNode(
                "This is text with no matching_ beginning delimiter", TextType.TEXT
            )
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_front_text(self):
        node = TextNode(
            "`This is text with a` code block at the beginning", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a", TextType.CODE),
                TextNode(" code block at the beginning", TextType.TEXT),
            ],
        )

    def test_end_text(self):
        node = TextNode("This is text with a **bold word at the end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold word at the end", TextType.BOLD),
            ],
        )

    def test_returns_list(self):
        node = TextNode("This is text with a **BOLD** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIsInstance(new_nodes, list)

    def test_multiple_delimiters(self):
        node = TextNode(
            "This is a **bold text** with a `code block` _italic word_", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_new_new_nodes = split_nodes_delimiter(new_new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with a `code block` _italic word_", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" _italic word_", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_new_new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_not_text_type(self):
        node = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        split_node = split_nodes_image([node])
        self.assertEqual(split_node, [node])

    def test_has_mixed_nodes(self):
        nodes = [
            TextNode(
                "This is a node with a ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT,
            ),
            TextNode(" and this is bold", TextType.BOLD),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is a node with a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and this is bold", TextType.BOLD),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_just_text(self):
        node = TextNode("This is text", TextType.TEXT)
        nodes = [
            TextNode("This is text", TextType.TEXT),
            TextNode(" and this is more text", TextType.TEXT),
        ]
        new_node = split_nodes_image([node])
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
            ],
            new_node,
        )
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
                TextNode(" and this is more text", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_image(self):
        matches = extract_markdown_images("This is text with no image")
        self.assertListEqual([], matches)

    def test_no_link(self):
        matches = extract_markdown_links("This is text with no link")
        self.assertListEqual([], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_only_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def text_extract_only_image(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_not_text_type(self):
        node = TextNode("link", TextType.LINK, "https://www.boot.dev")
        split_node = split_nodes_link([node])
        self.assertEqual(split_node, [node])

    def test_has_mixed_nodes(self):
        nodes = [
            TextNode(
                "This is a node with a [link](https://www.boot.dev)",
                TextType.TEXT,
            ),
            TextNode(" and this is bold", TextType.BOLD),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is a node with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and this is bold", TextType.BOLD),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_just_text(self):
        node = TextNode("This is text", TextType.TEXT)
        nodes = [
            TextNode("This is text", TextType.TEXT),
            TextNode(" and this is more text", TextType.TEXT),
        ]
        new_node = split_nodes_link([node])
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
            ],
            new_node,
        )
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
                TextNode(" and this is more text", TextType.TEXT),
            ],
            new_nodes,
        )


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
