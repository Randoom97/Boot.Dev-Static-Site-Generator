from enum import Enum

from texthandling import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type: TextType):
    new_nodes = []
    for old_node in old_nodes:
        # an even number of parts means we encountered an unclosed section
        # for now we just asume it's closed at the end
        parts = old_node.text.split(delimiter)
        for index, part in enumerate(parts):
            if len(part) == 0:
                continue
            type = old_node.text_type if index % 2 == 0 else text_type
            new_nodes.append(TextNode(part, type))
    return new_nodes

def __split_nodes(old_nodes: list[TextNode], extract_func, text_type: TextType, offsets):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_func(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for image in images:
            start_index = text.index(image[0]) - offsets[0]
            end_index = text.index(image[1]) + len(image[1]) + offsets[1]
            pre_text = text[:start_index]
            post_text = text[end_index:]
            if len(pre_text) > 0:
                new_nodes.append(TextNode(pre_text, old_node.text_type))
            new_nodes.append(TextNode(image[0], text_type, image[1]))
            text = post_text
        if len(text) > 0:
            new_nodes.append(TextNode(text, old_node.text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    return __split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE, (2,1)) # 2 = len("!["), 1 = len(")")

def split_nodes_link(old_nodes: list[TextNode]):
    return __split_nodes(old_nodes, extract_markdown_links, TextType.LINK, (1,1)) # 1 = len("[", 1 = len(")")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes