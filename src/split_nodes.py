from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links


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


def partition_text(text, delimiters, text_type):
    result = []
    remaining = text

    while remaining:
        for text_alt, text_link in delimiters:
            delimiter = ""
            if text_type == TextType.LINK:
                delimiter = f"[{text_alt}]({text_link})"
            elif text_type == TextType.IMAGE:
                delimiter = f"![{text_alt}]({text_link})"
            before, sep, after = remaining.partition(delimiter)
            if sep:
                if before:
                    result.append(before)
                result.append(sep)
                remaining = after
            else:
                result.append(before)
                remaining = ""
    return result


def create_text_node_with_links(text, text_type):
    new_nodes = []

    for i in range(len(text)):
        if text[i] == "":
            continue
        elif i % 2 == 1:
            text_alt, text_link = ("", "")
            if text_type == TextType.IMAGE:
                text_alt, text_link = extract_markdown_images(text[i])[0]
            elif text_type == TextType.LINK:
                text_alt, text_link = extract_markdown_links(text[i])[0]
            new_nodes.append(
                TextNode(text=text_alt, text_type=text_type, url=text_link)
            )
        elif i % 2 == 0:
            new_nodes.append(TextNode(text[i], TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    if not old_nodes:
        return []
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            continue
        split_text = partition_text(node.text, images, TextType.IMAGE)

        new_nodes.extend(create_text_node_with_links(split_text, TextType.IMAGE))
    return new_nodes


def split_nodes_link(old_nodes):
    if not old_nodes:
        return []
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            continue
        split_text = partition_text(node.text, links, TextType.LINK)
        new_nodes.extend(create_text_node_with_links(split_text, TextType.LINK))
    return new_nodes
