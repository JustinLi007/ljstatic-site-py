import unittest
from htmlnode import DocTags
from textnode import (
    TextNode,
    is_delimiter,
    split_by_delimiter,
    split_nodes_delimiter,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("text", "bold", None)
        node2 = TextNode("text", "bold", None)
        self.assertEqual(node, node2)

    def test_none_object(self):
        node = TextNode("text", "bold", "url")
        node2 = None
        self.assertNotEqual(node, node2)

    def test_diff_textnode(self):
        node = TextNode("text", "bold", "url")
        node2 = TextNode("idff", "bold", "url")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
                "This is a text node", text_type_italic, "https://www.boot.dev"
                )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
                "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
                )

    def test_is_delimiter_double_asterisk(self):
        text = "** word **"
        delimiter = "**"
        idx1 = 0
        idx2 = 8
        result1 = is_delimiter(text, idx1, delimiter)
        result2 = is_delimiter(text, idx2, delimiter)
        finalResult = result1 and result2
        self.assertTrue(
                finalResult, f"""Text: {text}, Delimiter: {delimiter},
                Idx:{idx1}, {idx2}"""
                )

    def test_is_delimiter_no_closing_match(self):
        text = "** word *"
        delimiter = "**"
        idx1 = 0
        idx2 = 8
        result1 = is_delimiter(text, idx1, delimiter)
        result2 = is_delimiter(text, idx2, delimiter)
        finalResult = result1 and not result2
        self.assertTrue(
                finalResult, f"""Text: {text}, Delimiter: {delimiter},
                Idx:{idx1}, {idx2}"""
                )

    def test_split_by_delimiter_one_block(self):
        text = "This is a text with a `code block` in it"
        delimiter = '`'
        expected = ["This is a text with a ", "code block", " in it"]
        result = split_by_delimiter(text, "`")
        self.assertTrue(len(expected) == len(result), f"""Unexpected result length:
        Expected - {expected}, Actual - {result}
        """)
        for i in range(len(result)):
           self.assertEqual(result[i][0], expected[i])

    def test_split_by_delimiter_two_blocks(self):
        text = "This is a text with a `code block` and another `code block` in it"
        delimiter = '`'
        expected = ["This is a text with a ", "code block", " and another ",
                "code block", " in it"]
        result = split_by_delimiter(text, "`")
        self.assertTrue(len(expected) == len(result), f"""Unexpected result length:
        Expected - {expected}, Actual - {result}
        """)
        for i in range(len(result)):
           self.assertEqual(result[i][0], expected[i])

    def test_split_by_delimiter_end_block(self):
        text = "This is a text with a end `code block`"
        delimiter = '`'
        expected = ["This is a text with a end ", "code block"]
        result = split_by_delimiter(text, "`")
        self.assertTrue(len(expected) == len(result), f"""Unexpected result length:
        Expected - {expected}, Actual - {result}
        """)
        for i in range(len(result)):
           self.assertEqual(result[i][0], expected[i])

    def test_split_nodes_delimiter_one_block(self):
        old_nodes = [
                TextNode("This is a text with a `code block` in it", DocTags.TEXT)
                ]
        delimiter = '`'
        expected = [
                TextNode("This is a text with a ", DocTags.TEXT),
                TextNode("code block", DocTags.CODE),
                TextNode(" in it", DocTags.TEXT),
                ]
        result = split_nodes_delimiter(old_nodes, delimiter, DocTags.CODE)
        self.assertTrue(len(expected) == len(result), f"""Unexpected result length:
        Expected - {expected}, Actual - {result}
        """)
        for i in range(len(result)):
           self.assertEqual(result[i], expected[i])

    def test_split_nodes_delimiter_two_block(self):
        old_nodes = [
                TextNode("This is a text with a `code block` and another `code block` in it",
                    DocTags.TEXT)
                ]
        delimiter = '`'
        expected = [
                TextNode("This is a text with a ", DocTags.TEXT),
                TextNode("code block", DocTags.CODE),
                TextNode(" and another ", DocTags.TEXT),
                TextNode("code block", DocTags.CODE),
                TextNode(" in it", DocTags.TEXT),
                ]
        result = split_nodes_delimiter(old_nodes, delimiter, DocTags.CODE)
        self.assertTrue(len(expected) == len(result), f"""Unexpected result length:
        Expected - {expected}, Actual - {result}
        """)
        for i in range(len(result)):
           self.assertEqual(result[i], expected[i])

    def test_split_nodes_delimiter_end_block(self):
        old_nodes = [TextNode("This is a text with a end `code block`",
            DocTags.TEXT)]
        delimiter = '`'
        expected = [
                TextNode("This is a text with a end ", DocTags.TEXT),
                TextNode("code block", DocTags.CODE)
                ]
        result = split_nodes_delimiter(old_nodes, delimiter, DocTags.CODE)
        self.assertTrue(len(expected) == len(result), f"""Unexpected result length:
        Expected - {expected}, Actual - {result}
        """)
        for i in range(len(result)):
           self.assertEqual(result[i], expected[i])

if __name__ == "__main__":
    unittest.main()
