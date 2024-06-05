class HTMLNode():
    """
    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example,
        a link (<a> tag) might have {"href": "https://www.google.com"}
    """
    def __init__(self,tag = None,value = None,children = None,props = None):
        self.__tag = tag
        self.__value = value
        self.__children = children
        self.__props = props
    
    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML.")
    def props_to_html(self):
        # sample href="https://www.google.com" target="_blank"
        html = ""
        for prop in self.__props:
            html += f"{prop} "