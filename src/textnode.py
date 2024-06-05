"""
In textnode.py create a class called TextNode. It should have 3 properties that can be
 set in the constructor:

self.text - The text content of the node
self.text_type - The type of text this node contains, which is just a string like "bold" or "italic"
self.url - The URL of the link or image, if the text is a link. Default to None if nothing is passed 
in.
Next, create an __eq__ method that returns True if all of the properties of two TextNode objects are
 equal.

Finally, create a __repr__ method that returns a string representation of the TextNode object. 
It should look like this:

TextNode(TEXT, TEXT_TYPE, URL)
Copy icon
Where TEXT, TEXT_TYPE, and URL are the values of the text, text_type, and url properties, respectively.
"""

class TextNode():
    def __init__(self,text,text_type,url):
        self.__text = text
        self.__text_type = text_type
        self.__url = url

    def __eq__(self, other):
        return self.__text == other.__text and self.__text_type == other.__text_type and self.__url == other.__url
    
    def __repr__(self):
        return f"TextNode({self.__text}, {self.__text_type}, {self.__url})"
    