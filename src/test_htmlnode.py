import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node, markdown_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_all_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")

    def test_to_html_exception(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode(None, "something")
            ParentNode(None, [leaf]).to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("a", []).to_html()
    
    def test_to_html_none_children(self):
        with self.assertRaises(ValueError):
            ParentNode("a", None).to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_raw_leaf_to_html(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_no_value_leaf(self):
        with self.assertRaises(ValueError):
            LeafNode(None, None).to_html()

    def test_with_props(self):
        node = LeafNode("a", "google", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">google</a>")

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_text_type(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node(TextNode("asdf", "some invalid type")) # type: ignore
    
    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://some_url_to_an_image.com")
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://some_url_to_an_image.com", "alt": "alt text"})

    def test_link(self):
        node = TextNode("I'm google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "I'm google")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_bold(self):
        node = TextNode("boldly going where no man has gone before", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "boldly going where no man has gone before")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()