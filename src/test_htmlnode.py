import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None,None,None,{"href": "https://www.google.com", "target": "_blank"})
        leafNode = LeafNode("p", "This is a paragraph of text.")
        leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(leafNode.to_html(),'<p>This is a paragraph of text.</p>')
        self.assertEqual(leafnode2.to_html(),'<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()