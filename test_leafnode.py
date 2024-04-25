import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
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


if __name__ == "__main__":
    unittest.main()
