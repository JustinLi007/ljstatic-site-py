from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children == None:
            raise ValueError("Child nodes are required for parent node.")
        if self.tag == None:
            raise ValueError("Tag is required for parent node.")
        htmlElement = None
        openTag = f"<{self.tag}>"
        closingTag = f"</{self.tag}>"
        properties = self.props_to_html() 
        if not properties == None:
            openTag = f"{openTag[:-1]} {properties}>"

        childElements = []
        for child in self.children:
            childElements.append(child.to_html())

        htmlElement = f"""{openTag}{"".join(childElements)}{closingTag}"""

        return htmlElement
