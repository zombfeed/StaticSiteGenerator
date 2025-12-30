import re
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image_alt, image_link in images:
            delimiter = f"![{image_alt}]({image_link})"
            sections = original_text.split(delimiter)
            if len(sections) != 2:
                raise ValueError("Error: Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link_alt, link_link in links:
            delimiter = f"[{link_alt}]({link_link})"
            sections = original_text.split(delimiter)
            if len(sections) != 2:
                raise ValueError("Error: Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
