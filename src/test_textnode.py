import unittest

from textnode import TextNode, TextType, text_to_textnodes, split_nodes_delimiter, split_nodes_image, split_nodes_link
from texthandling import extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.url, None)

    def test_not_eq(self):
        node = TextNode("Have some text", TextType.TEXT)
        node2 = TextNode("Have some text", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        new_nodes = split_nodes_delimiter([TextNode("This is text with a `code block` word", TextType.TEXT)], '`', TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_bold(self):
        new_nodes = split_nodes_delimiter([TextNode("This is text with a **bold section**", TextType.TEXT)], '**', TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold section", TextType.BOLD)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_multiple_input(self):
        old_nodes = [
            TextNode("I'm a **bold section**", TextType.TEXT),
            TextNode("What a coincidence, I have a **bold section** too", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
        expected = [
            TextNode("I'm a ", TextType.TEXT),
            TextNode("bold section", TextType.BOLD),
            TextNode("What a coincidence, I have a ", TextType.TEXT),
            TextNode("bold section", TextType.BOLD),
            TextNode(" too", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_no_delimiter_in_input(self):
        old_nodes = [TextNode("I have no code", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)
        self.assertListEqual(old_nodes, new_nodes)

    def test_empty_input(self):
        self.assertListEqual(split_nodes_delimiter([], '`', TextType.CODE), [])
    
    def test_unclosed(self):
        new_nodes = split_nodes_delimiter([TextNode("I have unclosed _italic", TextType.TEXT)], '_', TextType.ITALIC)
        expected = [
            TextNode("I have unclosed ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ]
        self.assertListEqual(new_nodes, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_multiple_images(self):
        matches = extract_markdown_images(
            "![image1](img1_url) ![image2](img2_url)"
        )
        self.assertListEqual([("image1", "img1_url"), ("image2", "img2_url")], matches)

    def test_no_image(self):
        matches = extract_markdown_images("[i'm a link](link_url)")
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](link_url)"
        )
        self.assertListEqual([("link", "link_url")], matches)
    
    def test_multiple_links(self):
        matches = extract_markdown_links(
            "[link1](link1_url) [link2](link2_url)"
        )
        self.assertListEqual([("link1", "link1_url"), ("link2", "link2_url")], matches)

    def test_no_link(self):
        matches = extract_markdown_links("![i'm an image](image_url)")
        self.assertListEqual([], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_no_images(self):
        node = TextNode("No image, just a [link](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_no_nodes(self):
        self.assertListEqual(split_nodes_image([]), [])
    
    def test_multi_nodes(self):
        nodes = [
            TextNode("no image in this one", TextType.TEXT),
            TextNode("![image](image_url) starting this one", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("no image in this one", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "image_url"),
            TextNode(" starting this one", TextType.TEXT)
        ], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_links(self):
        node = TextNode(
            "This is text with a [link1](link1_url) and another [link2](link2_url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "link1_url"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK, "link2_url"
                ),
            ],
            new_nodes,
        )
    
    def test_no_links(self):
        node = TextNode("No link, just an ![image](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_no_nodes(self):
        self.assertListEqual(split_nodes_link([]), [])
    
    def test_multi_nodes(self):
        nodes = [
            TextNode("no link in this one", TextType.TEXT),
            TextNode("[link](link_url) starting this one", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual([
            TextNode("no link in this one", TextType.TEXT),
            TextNode("link", TextType.LINK, "link_url"),
            TextNode(" starting this one", TextType.TEXT)
        ], new_nodes)

class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()