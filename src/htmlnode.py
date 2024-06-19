class HTMLNode():
    """
    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example,
        a link (<a> tag) might have {"href": "https://www.google.com"}
    """
    def __init__(self,tag = None,value = None,children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML.")
    def props_to_html(self):
        # sample href="https://www.google.com" target="_blank"
        html = ""
        for prop, value in self.props.items():
            html += f' {prop}="{value}"'
        return html
    
    def __repr__(self) -> str:
        #print(self.__tag, self.__value, self.__children, self.__props)
        pass

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag == None:
            return self.value
        elif self.props == None:
            print(self.value)
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"  