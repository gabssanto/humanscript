# AST Node types
class ASTNode:
    pass


class PrintNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"PrintNode({self.value})"


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"StringNode({self.value})"


class VarAssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"VarAssignNode({self.name}, {self.value})"


class VarAccessNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"VarAccessNode({self.name})"


class VarDeclNode(ASTNode):
    def __init__(self, name, var_type):
        self.name = name
        self.var_type = var_type

    def __repr__(self) -> str:
        return f"VarDeclNode({self.name}, {self.var_type})"


class InputNode(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt

    def __repr__(self) -> str:
        return f"InputNode({self.prompt})"


class FuncDeclNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self) -> str:
        return f"FuncDeclNode({self.name}, {self.params}, {self.body})"


class FuncCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        return f"FuncCallNode({self.name}, {self.args})"
