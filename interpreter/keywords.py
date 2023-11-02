# # Keywords
# keywords = {
#     "tell",
#     "ask",
#     "gather",
#     "as",
#     "is",
#     "with",
#     "end",
#     "if",
#     "else",
#     "while",
#     "try",
#     "catch",
#     "String",
#     "Number",
#     "Boolean",
#     "Array",
#     "Dictionary",
#     "Class",
#     "Function",
#     "Bluetell",
#     "Type",
#     "init",
#     "extends",
#     "of",
#     "or",
#     "and",
# }

# keywords.py
from token_types import *

keywords = {
    "tell": TT_KEYWORD,
    "ask": TT_KEYWORD,
    "as": TT_KEYWORD,
    # ... other keywords ...
    "Function": TT_KEYWORD,
    "with": TT_KEYWORD,
    "do": TT_KEYWORD,
    "end": TT_KEYWORD,
    "String": TT_KEYWORD,
    "Number": TT_KEYWORD,
    "Boolean": TT_KEYWORD,
    "Array": TT_KEYWORD,
    "Dictionary": TT_KEYWORD,
    "call": TT_KEYWORD,
    # ... other keywords ...
}
