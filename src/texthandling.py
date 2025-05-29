import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def markdown_to_blocks(markdown):
    return list(filter(lambda b: len(b) != 0, map(lambda b: b.strip(), markdown.split("\n\n"))))

def block_to_block_type(block):
    if re.fullmatch(r"^#{1,6} .*$", block):
        return BlockType.HEADING
    if re.fullmatch(r"^```(.|\n)*```$", block):
        return BlockType.CODE
    if re.fullmatch(r"^(>.*\n)*(>.*)$", block):
        return BlockType.QUOTE
    if re.fullmatch(r"^(- .*\n)*(- .*)$", block):
        return BlockType.UNORDERED_LIST
    # "all" part is just checking that it starts at 1 and sequentially increases
    if re.fullmatch(r"^(\d+\. .*\n)*(\d+\. .*)$", block) and all(map(lambda iv: iv[0] == iv[1], enumerate(map(lambda l: int(l[:l.index('.')])-1, block.split('\n'))))):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def trim_line_leading_markdown(block, indicator):
    return '\n'.join(map(lambda l: l[l.index(indicator)+1:].strip(), block.split('\n')))

def extract_title(markdown):
    matches = re.match("# .*", markdown)
    if matches == None:
        raise Exception("couldn't find a title")
    return matches[0][2:].strip()
    