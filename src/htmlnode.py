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
        if self.props is None:
            return""
        html = ""
        for prop, value in self.props.items():
            html += f' {prop}="{value}"'
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if not isinstance(self.value, str):
            raise TypeError("LeafNode value must be a string")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"   
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if not isinstance(self.children, list):
            raise TypeError("ParentNode children must be a list")
        if self.tag is None:
            raise ValueError("HTML Error: Tag not provided.")
        if self.children is None:
            raise ValueError("HTML Error: Parent Node cant have no children.")
        html = ""
        for child in self.children:
            html += child.to_html()
        return f"<{self.tag}>{html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag},{self.children},{self.props})"