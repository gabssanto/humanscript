import sys
from lexer import lexer
from code_parser import Parser
from evaluator import Evaluator


# Main function to execute the interpreter
def main():
    # Check if a file name is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: dna <filename>.dna")
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
    # print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    # print(ast)
    evaluator = Evaluator()
    for node in ast:
        # print(node)
        evaluator.visit(node)


# Execute main function
if __name__ == "__main__":
    main()
