import re
from token_types import *

# Assume keywords is now a dictionary where the key is the keyword string and the value is the corresponding token type.
from keywords import keywords, operators


# Lexer: tokenize the input code
def lexer(code):
    tokens = []
    while code:
        match = None
        # Skip whitespaces
        if match := re.match(r"\s+", code):
            pass
        # Match boolean
        elif match := re.match(r"True|False", code):
            tokens.append((TT_BOOL, match.group(0)))
        # Match Type
        elif match := re.match(r"Type", code):
            tokens.append((TT_TYPE, match.group(0)))
        # Match keywords (including 'Function', 'do', 'end', 'with', etc.)
        elif match := re.match(r"[a-zA-Z_]\w*", code):
            identifier = match.group(0)
            if identifier in keywords:
                tokens.append((keywords[identifier], identifier))
            else:
                tokens.append((TT_IDENTIFIER, identifier))
        # Match operators
        elif match := re.match(r"==|!=|<=|>=|&&|\|\||[+\-*/%<>()]", code):
            operator = match.group(0)
            if operator in operators:
                tokens.append((operators[operator], operator))
            else:
                tokens.append(
                    (TT_OPERATOR, operator)
                )  # Fallback, in case operator is not in the dictionary
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
