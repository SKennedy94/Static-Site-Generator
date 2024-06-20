from htmlnode import *
from textnode import *

def main():

    node = TextNode("This is text with a `code block` word", text_types.text)

    new_nodes = split_nodes_delimiter([node], "`", text_types.code)
    print(new_nodes)

main()

