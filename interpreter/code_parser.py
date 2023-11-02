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

    def peek(self, step=1):
        # Look ahead at the next token without consuming the current one
        next_pos = self.pos + step
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

    def statements(self):
        statements = []
        while self.current_token is not None and self.current_token[1] != "end":
            # print(self.current_token)
            if self.current_token[1] == "tell":
                statements.append(self.tell_statement())
            elif self.current_token[1] == "ask":
                statements.append(self.ask_statement())
            elif self.current_token[1] == "call":
                statements.append(self.func_call())
            elif self.current_token[0] == TT_IDENTIFIER:
                if self.peek() == (TT_KEYWORD, "as"):
                    # statements.append(self.var_declaration())
                    # Check if the next keyword is 'Function', indicating a function declaration
                    if self.peek(2) == (TT_KEYWORD, "Function"):
                        statements.append(self.func_declaration())
                    else:
                        statements.append(self.var_declaration())

                else:
                    # Handle variable assignment or other expressions that start with an identifier
                    pass
            else:
                # Handle other kinds of statements or expressions
                pass
            self.advance()  # Make sure to only call this once per loop to keep the token stream moving forward
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

                    if self.current_token[1] == "ask":
                        # If the next token is 'ask', then we are expecting an input prompt
                        self.advance()
                        if self.current_token[0] != TT_STRING:
                            raise Exception(
                                "Expected string literal for the input prompt"
                            )
                        prompt = self.current_token[1]
                        return VarAssignNode(var_name, InputNode(prompt))

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

    def func_declaration(self):
        # print("func declaration", self.current_token)
        if self.current_token[0] != TT_IDENTIFIER:
            raise Exception("Expected function name before 'Function' keyword")

        func_name = self.current_token[1]
        self.advance()  # Consume Function name

        if self.current_token[1] != "as":
            raise Exception("Expected 'as' after function name")

        self.advance()  # Consumes 'as'

        # TODO: Later change to Callable type eg. String() so auto inference can be done
        if self.current_token[1] != "Function":
            raise Exception(
                f"Expected return type after 'as', returned {self.current_token[1]}"
            )

        return_type = self.current_token[1]
        self.advance()  # Consumes 'Function'
        # print("func declaration", self.current_token, func_name, return_type)

        # Handle parameters
        params = []
        while self.current_token[1] != "do":
            if self.current_token[1] == "with" or self.current_token[1] == ",":
                self.advance()  # Consume 'with' or ','

            var_name = self.current_token[1]
            self.advance()  # Consume parameter_name

            if self.current_token[1] != "as":
                raise Exception("Expected 'as' after parameter name")
            self.advance()  # Consume 'as'

            if self.current_token[0] != TT_KEYWORD:
                raise Exception("Expected type after 'as'")

            var_type = self.current_token[1]
            params.append((var_name, var_type))
            self.advance()  # Consume type

        self.advance()  # Consume 'do'

        # Parse the function body
        body = self.statements()

        if self.current_token is None or self.current_token[1] != "end":
            raise Exception("Expected 'end' after function body")
        # self.advance()  # Consume 'end'

        return FuncDeclNode(func_name, params, body)

    def func_call(self):
        # Consume 'call' keyword
        if self.current_token[1] != "call":
            raise Exception("Expected 'call' to invoke a function")
        self.advance()

        # Consume function name
        if self.current_token[0] != TT_IDENTIFIER:
            raise Exception("Expected function name after 'call'")
        func_name = self.current_token[1]
        self.advance()

        # Parse arguments - expecting at least one argument
        args = []
        if self.current_token and self.current_token[0] in [
            TT_STRING,
            TT_NUMBER,
            TT_IDENTIFIER,
        ]:
            args.append(self.current_token[1])
            self.advance()

            # Consume any additional arguments separated by commas
            while self.current_token and self.current_token[0] == TT_COMMA:
                self.advance()  # consume the comma
                if self.current_token[0] not in [TT_STRING, TT_NUMBER, TT_IDENTIFIER]:
                    raise Exception(
                        "Expected a string, number, or identifier as argument"
                    )
                args.append(self.current_token[1])

        return FuncCallNode(func_name, args)
