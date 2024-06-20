import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None,None,None,{"href": "https://www.google.com", "target": "_blank"})
        leafNode = LeafNode("p", "This is a paragraph of text.")
        leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        parentnode = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)

        parentnode2 = ParentNode(
        "p",
        [
            ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(leafNode.to_html(),'<p>This is a paragraph of text.</p>')
        self.assertEqual(leafnode2.to_html(),'<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(parentnode.to_html(),'<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        self.assertEqual(parentnode2.to_html(),'<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</p>')

if __name__ == "__main__":
    unittest.main()