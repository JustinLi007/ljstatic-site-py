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

    def test_markdown_to_html_5(self):
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

if __name__ == "__main__":
    unittest.main()
