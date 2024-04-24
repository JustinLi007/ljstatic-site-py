import unittest

from parentnode import ParentNode
from leafnode import LeafNode

leafNodes = [
        LeafNode("Bold text","b"),
        LeafNode("Normal text", None),
        LeafNode("italic text", "i"),
        LeafNode("Normal text", None),
        ]

class TestParentNode(unittest.TestCase):
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
