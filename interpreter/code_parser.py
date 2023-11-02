from token_types import *
from lexer import lexer
from ast_nodes import *


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
        if self.current_token[0] == TT_STRING:
            return PrintNode(StringNode(self.current_token[1]))
        elif self.current_token[0] == TT_IDENTIFIER:
            var_name = self.current_token[1]
            return PrintNode(VarAccessNode(var_name))  # Create a variable access node
        else:
            raise Exception('Expected string or variable name after "tell"')

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

                if (
                    self.current_token is not None
                    and self.current_token[0] == TT_ASSIGN
                ):
                    self.advance()  # Consume '='

                    # Now expecting a value for initialization
                    if self.current_token[0] in (TT_STRING, TT_NUMBER):
                        value = self.current_token[1]

                        return VarAssignNode(
                            var_name, value
                        )  # Use a VarAssignNode to assign the initial value
                    else:
                        raise Exception(
                            "Expected a value for variable initialization after '='"
                        )
                else:
                    # If there's no '=', proceed with declaration without initialization
                    return VarDeclNode(var_name, var_type)

            else:
                raise Exception("Expected type keyword after 'as'")
        else:
            raise Exception("Expected 'as' after variable name")
