import unittest

from markdown import markdown_to_html_node

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_html_empty_markdown(self):
        markdown = (
                ""
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div></div>")
        self.assertEqual(expected, repr(actual))

    def test_markdown_to_html_2(self):
        markdown = (
                "### Header 3\n\n"
                "This is a regular paragraph"
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div><h3>Header 3</h3><p>This is a regular paragraph</p></div>")
        self.assertEqual(expected, repr(actual))

    def test_markdown_to_html_3(self):
        markdown = (
                "### Header 3\n\n"
                "This is a regular paragraph\n\n"
                "```This is a block of code```"
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div><h3>Header 3</h3><p>This is a regular paragraph</p>"
                "<pre><code>This is a block of code</code></pre>"
        "</div>")
        self.assertEqual(expected, repr(actual))

    def test_markdown_to_html_4(self):
        markdown = (
                "### Header 3\n\n"
                "This is a regular paragraph\n\n"
                "```This is a block of code```\n\n"
                ">This is a quote"
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div><h3>Header 3</h3><p>This is a regular paragraph</p>"
                "<pre><code>This is a block of code</code></pre>"
                "<blockquote>This is a quote</blockquote>"
        "</div>")
        self.assertEqual(expected, repr(actual))

    def test_markdown_to_html_5(self):
        markdown = (
                "### Header 3\n\n"
                "This is a regular paragraph\n\n"
                "```This is a block of code```\n\n"
                ">This is a quote\n\n"
                "* ul item 1\n"
                "* ul item 2\n"
                "* ul item 3\n"
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div><h3>Header 3</h3><p>This is a regular paragraph</p>"
                "<pre><code>This is a block of code</code></pre>"
                "<blockquote>This is a quote</blockquote>"
                "<ul>"
                "<li>ul item 1</li>"
                "<li>ul item 2</li>"
                "<li>ul item 3</li>"
                "</ul>"
        "</div>")
        self.assertEqual(expected, repr(actual))

    def test_markdown_to_html_6(self):
        markdown = (
                "### Header 3\n\n"
                "This is a regular paragraph\n\n"
                "```This is a block of code```\n\n"
                ">This is a quote\n\n"
                "* ul item 1\n"
                "* ul item 2\n"
                "* ul item 3\n\n"
                "1. ul item 1\n"
                "2. ul item 2\n"
                "3. ul item 3\n"
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div><h3>Header 3</h3><p>This is a regular paragraph</p>"
                "<pre><code>This is a block of code</code></pre>"
                "<blockquote>This is a quote</blockquote>"
                "<ul>"
                "<li>ul item 1</li>"
                "<li>ul item 2</li>"
                "<li>ul item 3</li>"
                "</ul>"
                "<ol>"
                "<li>ul item 1</li>"
                "<li>ul item 2</li>"
                "<li>ul item 3</li>"
                "</ol>"
        "</div>")
        self.assertEqual(expected, repr(actual))

    def test_markdown_to_html_7(self):
        codeBlock = ("```\n"
                "This is a block of code\n"
                "This is the second line of code\n"
                "This is the third line of code\n"
                "```\n\n")
        markdown = (
                "### Header 3\n\n"
                "This is a regular paragraph\n\n"
                f"{codeBlock}"
                ">This is a quote"
                )
        actual = markdown_to_html_node(markdown)
        expected = ("<div><h3>Header 3</h3><p>This is a regular paragraph</p>"
                "<pre><code>"
                "This is a block of code\n"
                "This is the second line of code\n"
                "This is the third line of code"
                "</code></pre>"
                "<blockquote>This is a quote</blockquote>"
        "</div>")
        self.assertEqual(expected, repr(actual))

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        self.assertEqual(
                repr(node),
                ("<div><p>This is <b>bolded</b> paragraph text in a p tag"
                    " here</p></div>"),
                )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        self.assertEqual(
                repr(node),
                ("<div><p>This is <b>bolded</b> paragraph text in a p tag"
                    " here</p><p>This is another paragraph with <i>italic</i>"
                    " text and <code>code</code> here</p></div>"),
                )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        self.assertEqual(
                repr(node),
                (
                "<div><ul><li>This is a list</li><li>with items</li><li>and"
                " <i>more</i> items</li></ul><ol><li>This is an"
                " <code>ordered</code> list</li><li>with items</li><li>and more"
                " items</li></ol></div>"),
                )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        self.assertEqual(
                repr(node),
                ("<div><h1>this is an h1</h1><p>this is paragraph"
                    " text</p><h2>this is an h2</h2></div>"),
                )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        self.assertEqual(
                repr(node),
                ("<div><blockquote> This is a blockquote"
                    " block</blockquote><p>this is paragraph text</p></div>"),
                )

if __name__ == "__main__":
    unittest.main()
