from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image
import split_nodes
from textnode import TextType, TextNode


def text_to_textnodes(text):
    new_nodes = []
    node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([node], "**", TextType.BOLD),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
