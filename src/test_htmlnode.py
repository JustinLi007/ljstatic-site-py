import unittest

from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode 
from markdown import text_node_to_html_node
from markdown_types import DocTags

leafNodes = [
        LeafNode("Bold text","b"),
        LeafNode("Normal text", None),
        LeafNode("italic text", "i"),
        LeafNode("Normal text", None),
        ]

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlNode = HTMLNode("h1", "header", leafNodes, {"href":"url",
            "target":"_blank"})
        expected = """<h1 href="url" target="_blank">header<b>Bold text</b>Normal text<i>italic text</i>Normal text</h1>"""
        self.assertEqual(repr(htmlNode), expected)

    def test_tag_only_html_node(self):
        htmlNode = HTMLNode("h1", None,  None, None)
        expected = """<h1></h1>"""
        self.assertEqual(repr(htmlNode), expected)

    def test_value_only_html_node(self):
        htmlNode = HTMLNode(None, "header", None, None)
        expected = """header"""
        self.assertEqual(repr(htmlNode), expected)

    def test_tag_n_children_only(self):
        htmlNode = HTMLNode("h1", None, leafNodes, None)
        expected = """<h1><b>Bold text</b>Normal text<i>italic text</i>Normal text</h1>"""
        self.assertEqual(repr(htmlNode), expected)
        
    def test_tag_n_props_only(self):
        htmlNode = HTMLNode("h1", None, None, {"href":"url",
            "target":"_blank"})
        expected = """<h1 href="url" target="_blank"></h1>"""
        self.assertEqual(repr(htmlNode), expected)

    def test_text_to_html_node_text_empty_content(self):
        textNode = TextNode("  ", DocTags.TEXT, None)
        leafNode = text_node_to_html_node(textNode)
        expected = "  "
        self.assertEqual(repr(leafNode), expected)

    def test_text_to_html_node_text(self):
        textNode = TextNode("text content", DocTags.TEXT, None)
        leafNode = text_node_to_html_node(textNode)
        expected = "text content"
        self.assertEqual(repr(leafNode), expected)

    def test_text_to_html_node_bold(self):
        textNode = TextNode("text content", DocTags.BOLD, None)
        leafNode = text_node_to_html_node(textNode)
        expected = "<b>text content</b>"
        self.assertEqual(repr(leafNode), expected)

    def test_text_to_html_node_italic(self):
        textNode = TextNode("text content", DocTags.ITALIC, None)
        leafNode = text_node_to_html_node(textNode)
        expected = "<i>text content</i>"
        self.assertEqual(repr(leafNode), expected)

    def test_text_to_html_node_code(self):
        textNode = TextNode("text content", DocTags.CODE, None)
        leafNode = text_node_to_html_node(textNode)
        expected = "<code>text content</code>"
        self.assertEqual(repr(leafNode), expected)

    def test_text_to_html_node_link(self):
        textNode = TextNode("text content", DocTags.LINK, "https://google.com")
        leafNode = text_node_to_html_node(textNode)
        expected = """<a href="https://google.com">text content</a>"""
        self.assertEqual(repr(leafNode), expected)

    def test_text_to_html_node_img(self):
        textNode = TextNode("alt text", DocTags.IMAGE, "pic.jpeg")
        leafNode = text_node_to_html_node(textNode)
        expected = """<img src="pic.jpeg" alt="alt text"></img>"""
        self.assertEqual(repr(leafNode), expected)

    def test_to_html_leaf_node(self):
        leafNode = LeafNode("para", "p", {"class":"row"})
        expected = "<p class=\"row\">para</p>"
        self.assertEqual(repr(leafNode), expected)

    def test_value_only(self):
        leafNode = LeafNode("para", None, None)
        expected = "para"
        self.assertEqual(repr(leafNode), expected)

    def test_no_props(self):
        leafNode = LeafNode("para", "a", None)
        expected = "<a>para</a>"
        self.assertEqual(repr(leafNode), expected)

    def test_no_value(self):
        leafNode = LeafNode(None, "p", {"class":"row"})
        with self.assertRaises(ValueError):
            leafNode.to_html()
    
    def test_tag_only(self):
        leafNode = LeafNode(None, "p", None)
        with self.assertRaises(ValueError):
            leafNode.to_html()
    
    def test_props_only(self):
        leafNode = LeafNode(None, None, {"class":"row"})
        with self.assertRaises(ValueError):
            leafNode.to_html()

    def test_to_html(self):
        parentNode = ParentNode(leafNodes, "p", None)
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(repr(parentNode), expected)

    def test_to_html_with_props(self):
        parentNode = ParentNode(leafNodes, "p", {"class":"row"})
        expected = "<p class=\"row\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(repr(parentNode), expected)

#####

    def test_to_html_with_children(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode([child_node], "div")
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode([grandchild_node], "span")
        parent_node = ParentNode([child_node], "div")
        self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
                )

    def test_to_html_many_children(self):
        node = ParentNode(
                [
                    LeafNode("Bold text","b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                    ],
                "p"
                )
        self.assertEqual(
                node.to_html(),
                "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
                )

    def test_headings(self):
        node = ParentNode(
                [
                    LeafNode("Bold text","b"),
                    LeafNode("Normal text", None),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text", None),
                    ],
                "h2"
                )
        self.assertEqual(
                node.to_html(),
                "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
                )

if __name__ == "__main__":
    unittest.main()
