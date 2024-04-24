import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlNode = HTMLNode("h1", "header", "<children>", {"href":"url",
            "target":"_blank"})
        expected = """<h1 href="url" target="_blank">header<children></h1>"""
        self.assertEqual(repr(htmlNode), expected)

    def test_tag_only(self):
        htmlNode = HTMLNode("h1", None,  None, None)
        expected = """<h1></h1>"""
        self.assertEqual(repr(htmlNode), expected)

    def test_value_only(self):
        htmlNode = HTMLNode(None, "header", None, None)
        expected = """header"""
        self.assertEqual(repr(htmlNode), expected)

    def test_tag_n_children_only(self):
        htmlNode = HTMLNode("h1", None,  "<children>", None)
        expected = """<h1><children></h1>"""
        self.assertEqual(repr(htmlNode), expected)
        
    def test_tag_n_props_only(self):
        htmlNode = HTMLNode("h1", None, None, {"href":"url",
            "target":"_blank"})
        expected = """<h1 href="url" target="_blank"></h1>"""
        self.assertEqual(repr(htmlNode), expected)

if __name__ == "__main__":
    unittest.main()
