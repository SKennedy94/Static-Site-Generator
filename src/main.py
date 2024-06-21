from htmlnode import *
from textnode import *

def main():
    markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
    print(markdown_to_blocks(markdown))

main()

