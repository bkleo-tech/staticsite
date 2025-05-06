from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = re.split(image_pattern, node.text)
        # re.split with groups will alternate: [text, alt1, url1, text, alt2, url2, text, ...]

        i = 0
        while i < len(parts):
            if parts[i] == "":
                i += 1
                continue
            if (i + 2) < len(parts):
                # [text, alt, url]
                if parts[i]:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                new_nodes.append(TextNode(parts[i + 1], TextType.IMAGE, parts[i + 2]))
                i += 3
            else:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
                i += 1

    return new_nodes
    

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = re.split(link_pattern, node.text)

        i = 0
        while i < len(parts):
            if parts[i] == "":
                i += 1
                continue
            if (i + 2) < len(parts):
                before_text = parts[i]
                link_text = parts[i + 1]
                link_url = parts[i + 2]

                if before_text.endswith("!"):
                    new_nodes.append(TextNode(before_text + f"[{link_text}]({link_url})", TextType.TEXT))
                else:
                    if before_text:
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

                i += 3
            else:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
                i += 1

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # If you're using split_nodes_delimiter for bold, italic, code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes