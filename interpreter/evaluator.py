from ast_nodes import *


# Evaluator: execute the AST
class Evaluator:
    def __init__(self):
        self.variables = {}
        self.variables_types = {}

    def visit(self, node):
        # If the node is a raw datatype, return it as is.
        if isinstance(
            node, (int, float, str)
        ):  # Add any other datatypes you need to handle
            return node

        # Otherwise, proceed with the visitor pattern.
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_PrintNode(self, node):
        value = self.visit(node.value)
        print(value)
        return value

    def visit_TypeNode(self, node):
        value = self.visit(node.value)
        return self.variables_types[value]

    def visit_VarAccessNode(self, node):
        var_name = node.name
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"Undefined variable '{var_name}'")

    def visit_StringNode(self, node):
        return node.value

    def visit_NumberNode(self, node):
        return node.value

    def visit_BooleanNode(self, node):
        return node.value

    def visit_TypeOfNode(self, node):
        return type(node.value).__name__

    def visit_InputNode(self, node):
        return input(node.prompt)

    def visit_VarAssignNode(self, node):
        if isinstance(node.value, ASTNode):
            value = self.visit(node.value)
        else:
            value = node.value  # Directly assign the value
        self.variables_types[node.name] = node.var_type
        self.variables[node.name] = value
        return value

    def visit_VarDeclNode(self, node):
        # Here, you would set the initial value of the variable based on the type
        # For simplicity, we will initialize all variables to None or an empty equivalent
        if node.var_type == "String":
            initial_value = ""
            self.variables_types[node.name] = "String"
        elif node.var_type == "Number":
            initial_value = 0
            self.variables_types[node.name] = "Number"
        elif node.var_type == "Boolean":
            initial_value = False
            self.variables_types[node.name] = "Boolean"
        # Add cases for other types
        else:
            initial_value = None
            self.variables_types[node.name] = "None"

        self.variables[node.name] = initial_value
        return initial_value

    def visit_FuncDeclNode(self, node):
        # Store the function in the variables with its name as the key
        self.variables[node.name] = {"params": node.params, "body": node.body}

    def visit_FuncCallNode(self, node):
        # Retrieve the function declaration
        func_name = node.name

        if func_name not in self.variables or not isinstance(
            self.variables[func_name], dict
        ):
            raise Exception(f"Undefined function '{func_name}'")

        func_decl = self.variables[func_name]
        params = func_decl["params"]
        body = func_decl["body"]

        # Check if the number of arguments matches the number of parameters
        if len(node.args) != len(params):
            raise Exception(
                f"Function '{func_name}' expects {len(params)} arguments, got {len(node.args)}"
            )

        # Create a new scope for function execution
        old_variables = self.variables
        self.variables = {**self.variables}  # Create a copy of the current scope

        # Assign arguments to parameters
        for param, arg in zip(params, node.args):
            if isinstance(arg, str):  # Or other raw datatypes
                # Convert raw datatype to corresponding ASTNode
                arg_node = StringNode(arg)
            else:
                arg_node = arg
            self.variables[param[0]] = self.visit(arg_node)

        # Execute the function body
        result = None
        for statement in body:
            result = self.visit(statement)

        # Restore the old scope
        self.variables = old_variables

        return result

    def visit_AddNode(self, node):
        return self.visit(node.left_node) + self.visit(node.right_node)

    def visit_MultiplyNode(self, node):
        return self.visit(node.left_node) * self.visit(node.right_node)

    def visit_SubtractNode(self, node):
        return self.visit(node.left_node) - self.visit(node.right_node)

    def visit_DivideNode(self, node):
        return self.visit(node.left_node) / self.visit(node.right_node)
