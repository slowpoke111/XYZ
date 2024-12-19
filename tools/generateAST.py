import os
import sys
from typing import List, Generic, TypeVar

R = TypeVar('R')

def define_visitor(writer, base_name: str, types: List[str]):
    """
    Generate the Visitor interface
    
    :param writer: File writer object
    :param base_name: Base class name (e.g., 'Expr')
    :param types: List of type definitions
    """
    # Start Visitor interface (generic)
    writer.write(f"    class Visitor(Generic[R]):\n")
    
    # Generate visit methods for each type
    for type_def in types:
        type_name = type_def.split(':')[0].strip()
        # Method signature follows Java-like pattern
        writer.write(f"        def visit{type_name}{base_name}(self, {base_name.lower()}: {type_name}) -> R:\n")
        writer.write("            pass\n\n")

def define_type(writer, base_name: str, class_name: str, field_list: str):
    """
    Generate a nested class definition for an AST node type
    
    :param writer: File writer object
    :param base_name: Base class name (e.g., 'Expr')
    :param class_name: Name of the current class being defined
    :param field_list: Comma-separated string of field definitions
    """
    # Class definition with explicit base class
    writer.write(f"    class {class_name}({base_name}):\n")
    
    # Constructor with type hints
    fields_with_types = [field.strip() for field in field_list.split(',') if field.strip()]
    constructor_params = []
    for field in fields_with_types:
        type_and_name = field.split()
        # Adjust type if needed
        param_type = type_and_name[0] if len(type_and_name) > 1 else 'Any'
        param_name = type_and_name[-1]
        constructor_params.append(f"{param_name}: {param_type}")
    
    # Constructor signature
    writer.write(f"        def __init__(self, {', '.join(constructor_params)}):\n")
    
    # Store parameters in fields
    for field in fields_with_types:
        type_and_name = field.split()
        name = type_and_name[-1]
        writer.write(f"            self.{name} = {name}\n")
    
    # If no fields, add pass
    if not fields_with_types:
        writer.write("            pass\n")
    
    # Add type-annotated fields
    writer.write("\n")
    for field in fields_with_types:
        type_and_name = field.split()
        type_hint = type_and_name[0] if len(type_and_name) > 1 else 'Any'
        name = type_and_name[-1]
        writer.write(f"        {name}: {type_hint}\n")
    
    # Visitor pattern: accept method
    writer.write("\n")
    writer.write("        def accept(self, visitor: 'Expr.Visitor[R]') -> R:\n")
    writer.write(f"            return visitor.visit{class_name}Expr(self)\n")

def define_ast(output_dir: str, base_name: str, types: List[str]):
    """
    Generate the full AST class hierarchy
    
    :param output_dir: Directory to write the output file
    :param base_name: Base class name (e.g., 'Expr')
    :param types: List of type definitions
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create file path
    path = os.path.join(output_dir, f"{base_name}.py")
    
    with open(path, 'w', encoding='utf-8') as writer:
        # File header
        writer.write("from typing import Any, Optional, Generic, TypeVar\n\n")
        
        # Type variable for generic return type
        writer.write("R = TypeVar('R')\n\n")
        
        # Base abstract class
        writer.write(f"class {base_name}:\n")
        writer.write("    \"\"\"Base class for Abstract Syntax Tree nodes\"\"\"\n")
        
        # Define Visitor interface
        define_visitor(writer, base_name, types)
        
        # Placeholder base accept method
        writer.write("\n")
        writer.write("    def accept(self, visitor: 'Visitor[R]') -> R:\n")
        writer.write("        raise NotImplementedError('Subclasses must implement accept')\n\n")
        
        # Generate nested classes for each type
        for type_def in types:
            # Split type definition into class name and fields
            parts = type_def.split(':')
            class_name = parts[0].strip()
            fields = parts[1].strip() if len(parts) > 1 else ""
            
            # Define the type
            define_type(writer, base_name, class_name, fields)

def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: generate_ast.py <output_directory>")
        sys.exit(64)
    
    output_dir = sys.argv[1]
    
    # Define the expression types (mirroring the Java example)
    expr_types = [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right"
    ]
    
    # Generate the AST classes
    define_ast(output_dir, "Expr", expr_types)
    print(f"Generated Expr.py in {output_dir}")

if __name__ == "__main__":
    main()