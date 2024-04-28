from htmlnode import DocTags
import re

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
    new_nodes = []
    for node in old_nodes:
        parts = []
        parts.extend(split_by_delimiter(node.text, delimiter))
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        for part in parts:
            new_nodes.append(
                    TextNode(part[0], text_type if part[1] else DocTags.TEXT)  
                    )
    return new_nodes 

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        imgLinkTups = extract_markdown_images(node.text)
        if not len(imgLinkTups):
            new_nodes.append(node)
            continue
        splits = None
        splitPartLen = 0
        offset = 0
        temp = node.text 
        for img in imgLinkTups:
            splits = temp.split(f"![{img[0]}]({img[1]})",1)
            if len(splits) > 0 and len(splits[0]) > 0:
                new_nodes.append(TextNode(splits[0], DocTags.TEXT))
                splitPartLen = len(splits[0])
                splits.pop(0)
            new_nodes.append(
                    TextNode(img[0], DocTags.IMAGE, img[1])
                    )
            offset = len(f"![{img[0]}]({img[1]})") + splitPartLen
            temp = temp[offset:]
        if not splits == None:
            for remaining in splits:
                if len(remaining) > 0:
                    new_nodes.append(TextNode(remaining, DocTags.TEXT))
    return new_nodes 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        linkTups = extract_markdown_links(node.text)
        if not len(linkTups):
            new_nodes.append(node)
            continue
        splits = None
        splitPartLen = 0
        offset = 0
        temp = node.text 
        for link in linkTups:
            splits = temp.split(f"[{link[0]}]({link[1]})",1)
            if len(splits) > 0 and len(splits[0]) > 0:
                new_nodes.append(TextNode(splits[0], DocTags.TEXT))
                splitPartLen = len(splits[0])
                splits.pop(0)
            new_nodes.append(
                    TextNode(link[0], DocTags.LINK, link[1])
                    )
            offset = len(f"[{link[0]}]({link[1]})") + splitPartLen
            temp = temp[offset:]
        if not splits == None:
            for remaining in splits:
                if len(remaining) > 0:
                    new_nodes.append(TextNode(remaining, DocTags.TEXT))
    return new_nodes 

def text_to_textnodes(text):
    if text == None:
        raise Exception("Invalid text value")
    if not len(text):
        return TextNode("", DocTags.TEXT)
    node = TextNode(text, DocTags.TEXT)
    boldNodes = split_nodes_delimiter([node], "**", DocTags.BOLD)
    italicNodes = split_nodes_delimiter(boldNodes ,"*", DocTags.ITALIC)
    codeNodes = split_nodes_delimiter(italicNodes, "`", DocTags.CODE)
    imageNodes = split_nodes_image(codeNodes)
    new_nodes = split_nodes_link(imageNodes)
    return temp if not len(new_nodes) else new_nodes
