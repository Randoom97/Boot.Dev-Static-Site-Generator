from textnode import TextNode, TextType, text_to_textnodes
from texthandling import BlockType, markdown_to_blocks, block_to_block_type, trim_line_leading_markdown

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return ' '.join(list(map(lambda kv: f"{kv[0]}=\"{kv[1]}\"", self.props.items())))

    def __repr__(self):
        string_repr = f"{self.__class__.__name__}(tag:{self.tag}, value:{self.value}, props:{self.props})"
        if self.children != None:
            string_repr += " Children = [\n"
            for child in self.children:
                string_repr += f"{child}\n"
            string_repr += "]"
        return string_repr
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("all parent nodes must have a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("all parent nodes must have at least one child")
        children_html = ''.join(list(map(lambda c: c.to_html(), self.children)))
        return f"<{self.tag}>{children_html}</{self.tag}>"
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag == None:
            return self.value
        props = ""
        if self.props != None:
            props = f" {self.props_to_html()}"
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
def text_node_to_html_node(text_node: TextNode):
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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise TypeError("unsupported text type")

def text_to_children(text):
    return list(map(lambda tn: text_node_to_html_node(tn), text_to_textnodes(text.replace('\n', ' '))))

def text_to_list_items(text):
    return list(map(lambda line: ParentNode("li", text_to_children(line)), text.split('\n')))

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                heading_size = block.index(' ')
                children.append(ParentNode(f"h{heading_size}", text_to_children(block[heading_size+1:])))
            case BlockType.CODE:
                # remove the leading and trailing ```
                children.append(ParentNode("pre", [text_node_to_html_node(TextNode(block[3:-3].strip()+'\n', TextType.CODE))]))
            case BlockType.QUOTE:
                children.append(ParentNode("blockquote", text_to_children(trim_line_leading_markdown(block, '>'))))
            case BlockType.UNORDERED_LIST:
                children.append(ParentNode("ul", text_to_list_items(trim_line_leading_markdown(block, '-'))))
            case BlockType.ORDERED_LIST:
                children.append(ParentNode("ol", text_to_list_items(trim_line_leading_markdown(block, '.'))))
    return ParentNode("div", children)