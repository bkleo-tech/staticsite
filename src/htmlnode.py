class HTMLNode():
    def __init__(self, tag =None, value =None, children =None, props =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self): 
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html 
    
    def __repr__(self) -> str:
        return f"HTMLNODE({self.tag}, {self.value}, Children: {self.children}, {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if (self.value is None):
            raise ValueError("invalid HTML: no value")
        if (self.tag is None):
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        results =""
        if self.tag is None:
            raise ValueError("No tag")
        if not self.children:
                raise ValueError("No children")
        for item in self.children:
            results += item.to_html()
        return f"<{self.tag}>{results}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"