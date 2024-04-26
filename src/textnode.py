from htmlnode import DocTags

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if other == None: return False 
        return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
                )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def is_delimiter(text, idx, delimiter):
    if (text == None or delimiter == None or idx < 0):
        return False
    n = len(delimiter)
    part = text[idx:idx+n]
    return part == delimiter

def split_by_delimiter(text, delimiter):
    if text == None or delimiter == None or len(text.strip()) == 0:
        return []
    if len(delimiter.strip()) == 0:
        return text.split(" ")

    splits = []
    anchor = 0
    start = None
    end = None
    for i in range(len(text)):
        if text[i] == delimiter[0] and is_delimiter(text, i, delimiter):
            if start == None: 
                start = i
                continue
            else:
                end = i 
                splits.append((anchor, start, False))
                anchor = end + len(delimiter) 
                splits.append((start, anchor, True))
                start = None
                end = None

    # no closing match
    if not start == None and end == None:
        raise Exception("Invalid Markdown syntax") 
    
    if len(splits) == 0:
        return [(text, False)]
    result = []
    for tup in splits:
        result.append((text[tup[0]:tup[1]].strip(delimiter), tup[2]))
    if not len(text[splits[-1][1]:]) == 0:
        result.append((text[splits[-1][1]:], False))
    return result 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    parts = []
    new_nodes = []
    for node in old_nodes:
        parts.extend(split_by_delimiter(node.text, delimiter))
    for part in parts:
        new_nodes.append(
                TextNode(part[0], text_type if part[1] else DocTags.TEXT)  
                )
    return new_nodes 
