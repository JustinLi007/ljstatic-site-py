class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return None
        attrs = []
        for key in self.props:
            attrs.append(f"{key}=\"{self.props[key]}\"")
        return " ".join(attrs)

    def __repr__(self):
        htmlElement = None
        openTag = f"<{self.tag}>" if not self.tag == None else self.tag
        closingTag = None
        properties = None
        innerText = self.value
        childNodes = None
        if not openTag == None:
            closingTag = f"</{self.tag}>"
            properties = self.props_to_html()
            if not properties == None:
                openTag = f"{openTag[:-1]} {properties}>"
            childNodes = ("".join(map(lambda x: x.to_html(), self.children)) if
                    not self.children == None else "")
            htmlElement = f"""{openTag}{innerText if not innerText == None
else''}{childNodes}{closingTag}"""
        if htmlElement == None:
            htmlElement = "" if innerText == None else innerText

        return htmlElement 
