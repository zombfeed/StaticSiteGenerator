from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = 0
    BOLD_TEXT = 1
    ITALIC_TEXT = 2
    CODE_TEXT = 3
    LINKS = 4
    IMAGES = 5


class TextNode:
    def __init__(self, text, text_type, url):
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
