import unittest

from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_is_none(self):
        node = HTMLNode(None, None, None, None)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_is_not_none(self):
        node = HTMLNode("h1", "This is an HTML node", ["testnode"], {"test": "node"})
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.children)
        self.assertIsNotNone(node.props)

    def test_is_htmlnode(self):
        node = HTMLNode("h1", "This is an HTML node")
        self.assertIsInstance(node, HTMLNode)

    def test_is_not_htmlnode(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotIsInstance(node, HTMLNode)


class TestLeafNode(unittest.TestCase):
    def test_is_not_none(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.props)

    def test_is_none(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertIsNone(node.children)

    def test_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '"<a href="https://www.google.com">Click me!</a>"'
        )

    def test_raises_value_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)
            node.to_html()


if __name__ == "__main__":
    unittest.main()
