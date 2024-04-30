from enum import Enum

class DocTags(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class BlockTypes(Enum):
    NORMAL = 1
    PARAGRAPH = 2
    HEADING = 3
    CODE = 4
    QUOTE = 5
    UNORDERED_LIST = 6
    ORDERED_LIST = 7
