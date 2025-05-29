import unittest

from texthandling import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_multiple_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_no_empty_blocks(self):
        md = "\n\n\n\n\n\n\n\n\n\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(
            block_to_block_type("###### I'm a heading"),
            BlockType.HEADING
        )

    def test_heading_with_more_than_6(self):
        self.assertNotEqual(
            block_to_block_type("####### I'm not a heading"),
            BlockType.HEADING
        )

    def test_code(self):
        self.assertEqual(
            block_to_block_type("``` I'm a code block \n with multiple \n lines ```"),
            BlockType.CODE
        )

    def test_invalid_code(self):
        self.assertNotEqual(
            block_to_block_type("```extra text after the code block should make me invalid``` hi there"),
            BlockType.CODE
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> every line\n> needs to start \n> witha '> '"),
            BlockType.QUOTE
        )

    def test_invalid_quote(self):
        self.assertNotEqual(
            block_to_block_type("> not every\nline in this\n> starts with a '> '"),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- this\n- is\n- an\n- unordered\n- list"),
            BlockType.UNORDERED_LIST
        )

    def test_invalid_unordered_list(self):
        self.assertNotEqual(
            block_to_block_type("- whoops\nI forgot a\n- hyphen\nsomewhere"),
            BlockType.UNORDERED_LIST
        )
    
    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. this\n2. is an\n3. ordered list"),
            BlockType.ORDERED_LIST
        )

    def test_invalid_ordered_list(self):
        self.assertNotEqual(
            block_to_block_type("1. the numbers\n2. aren't\n300. sequential"),
            BlockType.ORDERED_LIST
        )

if __name__ == "__main__":
    unittest.main()