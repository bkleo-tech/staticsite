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
        text = ""
        for key, value in self.props.items():
            text += f' {key}="{value}"'
        return text 
    
    def __eq__(self, other):
        return (
			self.tag == other.tag and
			self.value == other.value and
			self.children == other.children and
            self.props == other.props
		)    
    
    def __repr__(self) -> str:
        return f"Tag: {self.tag}  Value: {self.value}  Children: {self.children}  Props: {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if (self.value is None):
            raise ValueError
        if (self.tag is None):
            return f"{self.value}"
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"