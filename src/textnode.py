from enum import Enum


class TextType(Enum):
    PLAIN = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


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
