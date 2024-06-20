from enum import Enum
from htmlnode import LeafNode

class text_types(Enum):
    text = 1
    bold = 2
    italic = 3
    code = 4
    link = 5
    image = 6

class TextNode():
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.__text_type:
        case text_types.text:
            return LeafNode(None,text_node.text)
        case text_types.bold:
            return LeafNode("b",text_node.text)
        case text_types.italic:
            return LeafNode("i",text_node.text)
        case text_types.code:
            return LeafNode("code",text_node.text)
        case text_types.link:
            return LeafNode ("a",text_node.text,{"href": text_node.url})
        case text_types.image:
            return LeafNode ("img","",{"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    extra_nodes = []
    for node in old_nodes:
        #if node is a TextNode and has a text type of text
        if type(node) is TextNode and node.text_type is text_types.text:
            #split string by the delimitter
            temp = node.text.split(delimiter) 
            #check for a closing delimitter
            if len(temp) % 2 == 0:
                raise ValueError("Markdown Syntax Error: no closing inline element")
            else:
                for i in range(len(temp)):
                    print(i%2)
                    if i % 2 == 1:
                        new_nodes.append(TextNode(temp[i], text_type))
                    else:
                        new_nodes.append(TextNode(temp[i], text_types.text))
        else:
             extra_nodes.append(node)   
    return new_nodes 

def extract_markdown_images(text):
    pass

def extract_markdown_links(text):
    pass