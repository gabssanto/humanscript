import re
import sys

# Token types
TT_KEYWORD = "KEYWORD"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_OPERATOR = "OPERATOR"
TT_NUMBER = "NUMBER"
# Additional token types
TT_ASSIGN = "ASSIGN"
TT_EQUALS = "EQUALS"

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

# Lexer Operators
operators = {"+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "="}
# Add a comma and parenthesis to your operators.
operators.update({",", "(", ")"})


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
        # Match assignment
        elif match := re.match(r"=", code):
            tokens.append((TT_ASSIGN, match.group(0)))
        else:
            raise SyntaxError(f"Unknown sequence: {code}")
        code = code[match.end() :]
    return tokens


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


class VarDeclNode(ASTNode):
    def __init__(self, name, var_type):
        self.name = name
        self.var_type = var_type


class InputNode(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt


# Parser: create an AST from tokens
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        ast = self.statements()
        if self.current_token is not None:
            raise Exception("Unexpected token: " + self.current_token[1])
        return ast

    def peek(self):
        # Look ahead at the next token without consuming the current one
        next_pos = self.pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

    def statements(self):
        statements = []
        while self.current_token is not None and self.current_token[1] != "end":
            if self.current_token[1] == "tell":
                statements.append(self.tell_statement())
            elif self.current_token[1] == "ask":
                statements.append(self.ask_statement())
            elif self.current_token[0] == TT_IDENTIFIER:
                # Look ahead for 'as'
                if self.peek() == ("KEYWORD", "as"):
                    statements.append(self.var_declaration())
                else:
                    # Handle variable assignment or other expressions that start with an identifier
                    pass
            self.advance()
        return statements

    def tell_statement(self):
        self.advance()
        if self.current_token[0] != TT_STRING:
            raise Exception('Expected string after "tell"')
        return PrintNode(StringNode(self.current_token[1]))

    def ask_statement(self):
        self.advance()
        # Expecting a string literal for the input prompt
        if self.current_token[0] != TT_STRING:
            raise Exception("Expected string literal for the input prompt")
        prompt = self.current_token[1]

        # Advance past the string
        # self.advance()

        var_name = prompt

        # Return a VarAssignNode with the variable name and an InputNode
        return VarAssignNode(var_name, InputNode(prompt))

    def var_declaration(self):
        # Assume current token is the variable identifier
        var_name = self.current_token[1]
        self.advance()  # Consume identifier

        if self.current_token is not None and self.current_token[1] == "as":
            self.advance()  # Consume 'as'

            if self.current_token[0] == TT_KEYWORD and self.current_token[1] in {
                "String",
                "Number",
                "Boolean",
                "Array",
                "Dictionary",
            }:
                var_type = self.current_token[1]
                self.advance()  # Consume type
                return VarDeclNode(var_name, var_type)
            else:
                raise Exception("Expected type keyword after 'as'")
        else:
            raise Exception("Expected 'as' after variable name")


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

    def visit_InputNode(self, node):
        return input(node.prompt)

    def visit_VarAssignNode(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value
        return value

    def visit_VarDeclNode(self, node):
        # Here, you would set the initial value of the variable based on the type
        # For simplicity, we will initialize all variables to None or an empty equivalent
        if node.var_type == "String":
            initial_value = ""
        elif node.var_type == "Number":
            initial_value = 0
        # Add cases for other types
        else:
            initial_value = None

        self.variables[node.name] = initial_value
        return initial_value


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
