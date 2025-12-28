from re import split
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_node = []

    def create_text_node(text, delimiter, text_type):
        nodes_to_add = []
        if len(text) % 2 != 1:
            raise Exception(
                f"Error: Invalid Markdown, no matching closing delimiter ({delimiter})"
            )
        for i in range(len(text)):
            if text[i] == "":
                continue
            elif i % 2 == 1:
                nodes_to_add.append(TextNode(text[i], text_type))
            elif i % 2 == 0:
                nodes_to_add.append(TextNode(text[i], TextType.TEXT))
        return nodes_to_add

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_node.append(node)
            continue
        split_text = node.text.split(delimiter)
        nodes_to_add = create_text_node(split_text, delimiter, text_type)
        split_node.extend(nodes_to_add)
    return split_node
