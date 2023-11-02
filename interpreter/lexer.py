import re
from token_types import *

# Assume keywords is now a dictionary where the key is the keyword string and the value is the corresponding token type.
from keywords import keywords
from operators import operators


# Lexer: tokenize the input code
def lexer(code):
    tokens = []
    while code:
        match = None
        # Skip whitespaces
        if match := re.match(r"\s+", code):
            pass
        # Match keywords (including 'Function', 'do', 'end', 'with', etc.)
        elif match := re.match(r"[a-zA-Z_]\w*", code):
            identifier = match.group(0)
            if identifier in keywords:
                tokens.append((keywords[identifier], identifier))
            else:
                tokens.append((TT_IDENTIFIER, identifier))
        # Match operators
        elif match := re.match(r"==|!=|<=|>=|&&|\|\||[+\-*/<>]", code):
            tokens.append((TT_OPERATOR, match.group(0)))
        # Match strings
        elif match := re.match(r'"[^"]*"', code):
            tokens.append((TT_STRING, match.group(0)[1:-1]))  # Remove quotation marks
        # Match numbers
        elif match := re.match(r"\d+", code):
            tokens.append((TT_NUMBER, int(match.group(0))))
        # Match assignment
        elif match := re.match(r"=", code):
            tokens.append((TT_ASSIGN, match.group(0)))
        # Match comma
        elif match := re.match(r",", code):
            tokens.append((TT_COMMA, match.group(0)))
        else:
            raise SyntaxError(f"Unknown sequence: {code}")
        code = code[match.end() :]
    return tokens
