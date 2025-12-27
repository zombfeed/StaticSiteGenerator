from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError("Error: No text_type in given node")


class TextNode:
    """
    TextNode        : a 'node' representing the text of Markdown
    Required variables ----------------------------------------
        text        : a string representing the text content of the node
        text_type   : a string representing the TextType of the node
    Optional           ----------------------------------------
        url         : a dictionary of key-value pairs representing the attributes of the HTML tag
    """

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text, self.text_type, self.url) == (
            other.text,
            other.text_type,
            other.url,
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
