import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_html_is_none(self):
        node = HTMLNode(None, None, None, None)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_html_is_not_none(self):
        node = HTMLNode("h1", "This is an HTML node", ["testnode"], {"test": "node"})
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.children)
        self.assertIsNotNone(node.props)

    def test_html_is_htmlnode(self):
        node = HTMLNode("h1", "This is an HTML node")
        self.assertIsInstance(node, HTMLNode)

    def test_html_is_not_htmlnode(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotIsInstance(node, HTMLNode)


class TestLeafNode(unittest.TestCase):
    def test_leaf_is_not_none(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.props)

    def test_leaf__is_none(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertIsNone(node.children)

    def test_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '"<a href="https://www.google.com">Click me!</a>"'
        )

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_parent_is_not_none(self):
        node = ParentNode(
            "p", [LeafNode("b", "Bold text")], {"href": "https://www.google.com"}
        )
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.children)
        self.assertIsNotNone(node.props)

    def test_parent_is_none(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")])
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)

    def test_parent_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "Bold text")])
            node.to_html()

    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_to_html_with_multiple_grandchildren(self):
        child_node = ParentNode(
            "span",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>Bold text</b>Normal text<i>italic text</i>Normal text</span></div>",
        )


if __name__ == "__main__":
    unittest.main()
