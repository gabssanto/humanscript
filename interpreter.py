import re
import sys

# Token types
TT_KEYWORD = "KEYWORD"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_OPERATOR = "OPERATOR"
TT_NUMBER = "NUMBER"

# Keywords
keywords = {
    "tell",
    "ask",
    "gather",
    "as",
    "is",
    "with",
    "end",
    "if",
    "else",
    "while",
    "try",
    "catch",
    "String",
    "Number",
    "Boolean",
    "Array",
    "Dictionary",
    "Class",
    "Function",
    "Bluetell",
    "Type",
    "init",
    "extends",
    "of",
    "or",
    "and",
}

# Operators
operators = {"+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"}


# Lexer: tokenize the input code
def lexer(code):
    tokens = []
    while code:
        match = None
        # Skip whitespaces
        if match := re.match(r"\s+", code):
            pass
        # Match keywords and identifiers
        elif match := re.match(r"[a-zA-Z_]\w*", code):
            identifier = match.group(0)
            if identifier in keywords:
                tokens.append((TT_KEYWORD, identifier))
            else:
                tokens.append((TT_IDENTIFIER, identifier))
        # Match operators
        elif match := re.match(r"==|!=|<=|>=|&&|\|\||[+\-*/<>]", code):
            tokens.append((TT_OPERATOR, match.group(0)))
        # Match strings
        elif match := re.match(r'"[^"]*"', code):
            tokens.append((TT_STRING, match.group(0)[1:-1]))  # Remove quotation marks
        # Match integers
        elif match := re.match(r"\d+", code):
            tokens.append((TT_NUMBER, int(match.group(0))))
        else:
            raise SyntaxError(f"Unknown sequence: {code}")
        code = code[match.end() :]
    return tokens


# Additional token types
TT_ASSIGN = "ASSIGN"
TT_EQUALS = "EQUALS"


# AST Node types
class ASTNode:
    pass


class PrintNode(ASTNode):
    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value


class VarAssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class VarAccessNode(ASTNode):
    def __init__(self, name):
        self.name = name


# Parser: create an AST from tokens
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = (
            self.tokens[self.pos] if self.pos < len(self.tokens) else None
        )

    def parse(self):
        ast = self.statements()
        if self.current_token is not None:
            raise Exception("Unexpected token: " + self.current_token[1])
        return ast

    def statements(self):
        statements = []
        while self.current_token is not None and self.current_token[1] != "end":
            if self.current_token[1] == "tell":
                statements.append(self.tell_statement())
            self.advance()
        return statements

    def tell_statement(self):
        self.advance()
        if self.current_token[0] != TT_STRING:
            raise Exception('Expected string after "tell"')
        return PrintNode(StringNode(self.current_token[1]))


# Example usage:
code = 'tell "Hello World"'
tokens = lexer(code)
parser = Parser(tokens)
ast = parser.parse()
# print(ast)  # This should print a representation of the AST


# Evaluator: execute the AST
class Evaluator:
    def __init__(self):
        self.variables = {}

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name)
        return method(node)

    def visit_PrintNode(self, node):
        value = self.visit(node.value)
        print(value)
        return value

    def visit_StringNode(self, node):
        return node.value


# Main function to execute the interpreter
def main():
    # Check if a file name is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Read the content of the file
    try:
        with open(filename, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        sys.exit(1)

    # Lexing, parsing, and evaluation
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    evaluator = Evaluator()
    for node in ast:
        evaluator.visit(node)


# Execute main function
if __name__ == "__main__":
    main()

# # Execute AST
# evaluator = Evaluator()
# for node in ast:
#     evaluator.visit(node)

# # This will print "Hello World" to the console as a result of executing the AST
