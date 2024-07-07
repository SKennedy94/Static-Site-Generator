import re
from enum import Enum
from htmlnode import *

class text_types(Enum):
    text = 1
    bold = 2
    italic = 3
    code = 4
    link = 5
    image = 6

class block_types(Enum):
    paragraph = 0
    heading = 1
    code = 2
    quote = 3
    unordered_list = 4
    ordered_list = 5

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
    match text_node.text_type:
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
    for node in old_nodes:
        #if node is a TextNode and has a text type of text
        if isinstance(node, TextNode) and node.text_type is text_types.text:
            #split string by the delimitter
            splits = node.text.split(delimiter) 
            #check for a closing delimitter
            if len(splits) % 2 == 0:
                raise ValueError("Markdown Syntax Error: no closing inline element")
            else:
                for i, split_text in enumerate(splits):
                    if i % 2 == 1:
                        new_nodes.append(TextNode(split_text, text_type))
                    else:
                        new_nodes.append(TextNode(split_text, text_types.text))
        else:
             new_nodes.append(node)   
    return new_nodes 

def split_nodes_image(old_nodes):
    new_nodes = []

    if len(old_nodes) == 0:
        raise ValueError("old_nodes is an empty list.")

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == text_types.text:
            if node.text != "":
                # Find all Markdown images in the node's text
                matches = extract_markdown_images(node.text)

                if len(matches) == 0:
                    # If no matches found, just append the original node
                    new_nodes.append(TextNode(node.text, text_types.text))
                else:
                    temp = node.text
                    for alt, src in matches:
                        split_parts = temp.split(f"![{alt}]({src})", 1)
                        if(split_parts[0]) == "":
                            new_nodes.append(TextNode(alt,text_types.image,src))
                        else:
                            new_nodes.append(TextNode(split_parts[0],text_types.text))
                            new_nodes.append(TextNode(alt,text_types.image,src))
                        temp = split_parts[1]

                    if temp != "":
                        new_nodes.append(TextNode(temp,text_types.text))
        else:
            new_nodes.append(node)   
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    if len(old_nodes) == 0:
        raise ValueError("old_nodes is an empty list.")

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == text_types.text:
            if node.text != "":
                # Find all Markdown images in the node's text
                matches = extract_markdown_links(node.text)
                if len(matches) == 0:
                    # If no matches found, just append the original node
                    new_nodes.append(TextNode(node.text, text_types.text))
                else:
                    temp = node.text
                    for alt, src in matches:
                        split_parts = temp.split(f"[{alt}]({src})", 1)
                        if(split_parts[0]) == "":
                            new_nodes.append(TextNode(alt,text_types.link,src))
                        else:
                            new_nodes.append(TextNode(split_parts[0],text_types.text))
                            new_nodes.append(TextNode(alt,text_types.link,src))
                        temp = split_parts[1]

                    if temp != "":
                        new_nodes.append(TextNode(temp,text_types.text))

        else:
            new_nodes.append(node) 

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)

def text_to_textnodes(text):
    node = TextNode(text,text_types.text)
    test_nodes = [node]
    test_nodes = split_nodes_image(test_nodes)
    test_nodes = split_nodes_link(test_nodes)
    test_nodes = split_nodes_delimiter(test_nodes,'**',text_types.bold)
    test_nodes = split_nodes_delimiter(test_nodes,'*',text_types.italic)
    test_nodes = split_nodes_delimiter(test_nodes, '`', text_types.code)
    return test_nodes

def markdown_to_blocks(markdown):
    blocks = []
    block = []
    for line in markdown.split('\n'):
        if line == "":
            if len(block) != 0:
                blocks.append(block)
                block = []
        else:
            block.append(line)
    if len(block) != 0:
        blocks.append(block)
    return blocks

def block_to_block_type(block):

    if block[0].startswith('#'):
        return block_types.heading
    elif block[0].startswith('```') and block[len(block)-1].endswith('```'):
        return block_types.code
    elif block[0].startswith('*') or block[0].startswith('-'):
        is_unordered_block = True
        for i in range(len(block)):
            if block[i].startswith('*') or block[i].startswith('-'):
                is_unordered_block = True
            else:
                is_unordered_block = False
                break
        if is_unordered_block:
            return block_types.unordered_list

    for i in range(len(block)):
        if not block[i].startswith('>'):
            break
    else:
        return block_types.quote  

    for i in range(len(block)):
        if not block[i].startswith(f'{i+1}. '):
            break
    else:
        return block_types.ordered_list                        

    return block_types.paragraph

def paragraph_block_to_html_node(block):
    value = ""
    for line in block:
        value += line + '\n'
    text_nodes = text_to_textnodes(value)
    inline_nodes = []
    for node in text_nodes:
        inline_nodes.append(text_node_to_html_node(node))
    return ParentNode('p',inline_nodes)

def heading_block_to_html_node(block):
    header_index = block[0].count('#')
    value = ""
    if 1 > header_index > 6:
        raise ValueError(f"Markdown Error: invalid header index of h{header_index}")
    for line in block:
        value += line + '\n'
    text_nodes = text_to_textnodes(value[header_index:])
    inline_nodes = []
    for node in text_nodes:
        inline_nodes.append(text_node_to_html_node(node))
    return ParentNode(f'h{header_index}', inline_nodes)

def code_block_to_html_node(block):
    value = ""
    for line in block:
        value += line + '\n'
    text_nodes = text_to_textnodes(value[4:-4])
    inline_nodes = []
    for node in text_nodes:
        inline_nodes.append(text_node_to_html_node(node))
    return ParentNode('pre',[ParentNode('code',inline_nodes)])

def quote_block_to_html_node(block):
    value = ""
    for line in block:
        value += line[1:] + '\n'
    text_nodes = text_to_textnodes(value)
    inline_nodes = []
    for node in text_nodes:
        inline_nodes.append(text_node_to_html_node(node))

    return ParentNode('blockquote', inline_nodes)

def unordered_list_block_to_html_node(block):
    children = []
    for line in block:
        text_nodes = text_to_textnodes(line[2:])
        inline_nodes = []
        for node in text_nodes:
            inline_nodes.append(text_node_to_html_node(node))

        children.append(ParentNode('li',inline_nodes))
    return ParentNode('ul',children)

def ordered_list_block_to_html_node(block):
    children = []
    for line in block:
        text_nodes = text_to_textnodes(line[2:])
        inline_nodes = []
        for node in text_nodes:
            inline_nodes.append(text_node_to_html_node(node))

        children.append(ParentNode('li',inline_nodes))
    return ParentNode('ol',children)

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case block_types.paragraph:
                children.append(paragraph_block_to_html_node(block))
            case block_types.heading:
                children.append(heading_block_to_html_node(block))
            case block_types.code:
                children.append(code_block_to_html_node(block))
            case block_types.quote:
                children.append(quote_block_to_html_node(block))
            case block_types.unordered_list:
                children.append(unordered_list_block_to_html_node(block))
            case block_types.ordered_list:
                children.append(ordered_list_block_to_html_node(block))
    return ParentNode('div',children,)