import unittest
from htmlnode import DocTags
from textnode import (
    TextNode,
    is_delimiter,
    split_by_delimiter,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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
        
    def test_repr_whitespace_text(self):
        node = TextNode("  ", "type")
        self.assertEqual("""TextNode(  , type, None)""", repr(node))

    def test_repr_whitespace_none(self):
        node = TextNode("", "type")
        self.assertEqual("""TextNode(, type, None)""", repr(node))

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

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", DocTags.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", DocTags.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", DocTags.TEXT),
                    TextNode("bolded", DocTags.BOLD),
                    TextNode(" word", DocTags.TEXT),
                    ],
                new_nodes,
                )

    def test_delim_bold_double(self):
        node = TextNode(
                "This is text with a **bolded** word and **another**", DocTags.TEXT
                )
        new_nodes = split_nodes_delimiter([node], "**", DocTags.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", DocTags.TEXT),
                    TextNode("bolded", DocTags.BOLD),
                    TextNode(" word and ", DocTags.TEXT),
                    TextNode("another", DocTags.BOLD),
                    ],
                new_nodes,
                )

    def test_delim_bold_multiword(self):
        node = TextNode(
                "This is text with a **bolded word** and **another**", DocTags.TEXT
                )
        new_nodes = split_nodes_delimiter([node], "**", DocTags.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", DocTags.TEXT),
                    TextNode("bolded word", DocTags.BOLD),
                    TextNode(" and ", DocTags.TEXT),
                    TextNode("another", DocTags.BOLD),
                    ],
                new_nodes,
                )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", DocTags.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", DocTags.ITALIC)
        self.assertListEqual(
                [
                    TextNode("This is text with an ", DocTags.TEXT),
                    TextNode("italic", DocTags.ITALIC),
                    TextNode(" word", DocTags.TEXT),
                    ],
                new_nodes,
                )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", DocTags.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", DocTags.CODE)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", DocTags.TEXT),
                    TextNode("code block", DocTags.CODE),
                    TextNode(" word", DocTags.TEXT),
                    ],
                new_nodes,
                )

    def test_extract_markdown_images(self):
        text = """This text contains a image link
        ![Benjamin Bannekat](https://octodex.github.com/images/bannekat.png),
        ![Benjamin Bannekat](https://octodex.github.com/images/bannekat.png),
        ![Benjamin Bannekat](https://octodex.github.com/images/bannekat.png),
        wow."""
        actual = extract_markdown_images(text)
        expected = [
                ("Benjamin Bannekat","https://octodex.github.com/images/bannekat.png"),
                ("Benjamin Bannekat","https://octodex.github.com/images/bannekat.png"),
                ("Benjamin Bannekat","https://octodex.github.com/images/bannekat.png")
                ]
        self.assertListEqual(expected, actual)

    def test_extract_markdown_links(self):
        text = """This text contains a link
        [Benjamin Bannekat](https://octodex.github.com/images/bannekat.png),
        [Benjamin Bannekat](https://octodex.github.com/images/bannekat.png),
        [Benjamin Bannekat](https://octodex.github.com/images/bannekat.png),
        wow."""
        actual = extract_markdown_links(text)
        expected = [
                ("Benjamin Bannekat","https://octodex.github.com/images/bannekat.png"),
                ("Benjamin Bannekat","https://octodex.github.com/images/bannekat.png"),
                ("Benjamin Bannekat","https://octodex.github.com/images/bannekat.png")
                ]
        self.assertListEqual(expected, actual)

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://a.com/b.png) and another ![second image](https://c.com/d.png)",
                DocTags.TEXT
                )
        new_nodes = split_nodes_image([node])
        expected = [
                TextNode("This is text with an ", DocTags.TEXT),
                TextNode("image", DocTags.IMAGE,"https://a.com/b.png"),
                TextNode(" and another ", DocTags.TEXT),
                TextNode("second image", DocTags.IMAGE, "https://c.com/d.png")
                ]
        self.assertListEqual(expected, new_nodes)

    def test_split_nodes_image_none(self):
        node = TextNode("", DocTags.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("", DocTags.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_nodes_link(self):
        node = TextNode("This is text with an [image](https://a.com/b.png) and another [second image](https://c.com/d.png)",
                DocTags.TEXT
                )
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("This is text with an ", DocTags.TEXT),
                TextNode("image", DocTags.LINK,"https://a.com/b.png"),
                TextNode(" and another ", DocTags.TEXT),
                TextNode("second image", DocTags.LINK, "https://c.com/d.png")
                ]
        self.assertListEqual(expected, new_nodes)
        
    def test_split_nodes_link_none(self):
        node = TextNode("", DocTags.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("", DocTags.TEXT)]
        self.assertListEqual(expected, new_nodes)
        
    def test_split_image(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                DocTags.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("This is text with an ", DocTags.TEXT),
                    TextNode("image", DocTags.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    ],
                new_nodes,
                )

    def test_split_image_single(self):
        node = TextNode(
                "![image](https://www.example.com/image.png)",
                DocTags.TEXT
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [TextNode("image", DocTags.IMAGE, "https://www.example.com/image.png")],
                new_nodes
                )

    def test_split_images(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                DocTags.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("This is text with an ", DocTags.TEXT),
                    TextNode("image", DocTags.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", DocTags.TEXT),
                    TextNode(
                        "second image", DocTags.IMAGE, "https://i.imgur.com/3elNhQu.png"
                        )
                    ],
                new_nodes
                )

    def test_split_links(self):
        node = TextNode(
                "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
                DocTags.TEXT
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
                [
                    TextNode("This is text with a ", DocTags.TEXT),
                    TextNode("link", DocTags.LINK, "https://boot.dev"),
                    TextNode(" and ", DocTags.TEXT),
                    TextNode("another link", DocTags.LINK, "https://blog.boot.dev"),
                    TextNode(" with text that follows", DocTags.TEXT)
                    ],
                new_nodes
                )

    def test_text_to_textnodes(self):
        text = (
                "This is **text** with an *italic* word and a `code block` and an "
                "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets"
                "/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
                )
        expected = [
                TextNode("This is ", DocTags.TEXT),
                TextNode("text", DocTags.BOLD),
                TextNode(" with an ", DocTags.TEXT),
                TextNode("italic", DocTags.ITALIC),
                TextNode(" word and a ", DocTags.TEXT),
                TextNode("code block", DocTags.CODE),
                TextNode(" and an ", DocTags.TEXT),
                TextNode("image", DocTags.IMAGE,
                    ("https://storage.googleapis.com/qvault-webapp-dynamic-assets/"
                        "course_assets/zjjcJKZ.png")),
                    TextNode(" and a ", DocTags.TEXT),
                    TextNode("link", DocTags.LINK, "https://boot.dev")
                    ]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
