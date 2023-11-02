from ast_nodes import *


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

    def visit_VarAccessNode(self, node):
        var_name = node.name
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"Undefined variable '{var_name}'")

    def visit_StringNode(self, node):
        return node.value

    def visit_InputNode(self, node):
        return input(node.prompt)

    def visit_VarAssignNode(self, node):
        if isinstance(node.value, ASTNode):
            value = self.visit(node.value)
        else:
            value = node.value  # Directly assign the value
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

    def visit_FuncDeclNode(self, node):
        # Store the function in the variables with its name as the key
        self.variables[node.name] = {"params": node.params, "body": node.body}
