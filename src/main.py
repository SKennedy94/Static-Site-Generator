from htmlnode import *
from textnode import *

def main():
    markdown = """#This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

``` print("hello world")```
``` print("hello world")

> To be or not to be
that is the question

1. A
2. B
3. C

1. A
3. B

1. A
B"""
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        print(block_to_block_type(block))
    print(paragraph_block_to_html_node(blocks[1]))

main()

