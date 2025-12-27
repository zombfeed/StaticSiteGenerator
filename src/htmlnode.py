class HTMLNode:
    """
    HTMLNode        : represents a 'node' in an HTML document
    Member variables ----------------------------------------
        tag         : a string representing the HTML tag name
        value       : a string representing the value of the HTML tag
        children    : a list of HTMLNode objects representing the children of this node
        props       : a dictionary of key-value pairs representing the attributes of the HTML tag
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        rstring = ""
        for key, value in self.props.items():
            rstring += f" {key}='{value}'"
        return rstring

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
