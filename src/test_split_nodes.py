import unittest
from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image
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


if __name__ == "__main__":
    unittest.main()
