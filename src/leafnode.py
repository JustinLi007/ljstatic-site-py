from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Value required for leaf node.")
        htmlElement = None
        openTag = f"<{self.tag}>" if not self.tag == None else self.tag
        closingTag = None
        properties = None
        innerText = self.value
        if not openTag == None: 
            closingTag = f"</{self.tag}>"
            properties = self.props_to_html()
            if not properties == None:
                openTag = f"{openTag[:-1]} {properties}>"
            htmlElement = f"{openTag}{innerText}{closingTag}"
        if htmlElement == None:
            htmlElement = innerText

        return htmlElement
