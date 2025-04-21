from string import Template
import os
import importlib
import inspect
import pkgutil
import ast
from pathlib import Path

from ..globals import GLOBALS
from ..ne.btypes.node import Node
from ..ne.btypes.node_exec import NodeExec
from ..data.props_typed import WrappedPropertyDescriptor


TEMPLATE_NODE_TYPE = Template("""
@dataclass
class ${node_type_name}(NodeExec):
${fields}
${exec_func}
""")

TEMPLATE_NODE_EXEC_FUNC = Template("""
def execute(self, ${args}):
${body}
""")


SCRIPT_TEMPLATE = Template("""
# --- Imports ---
import bpy
from bpy import types as bpy_types
${imports}

# --- Globals ---
${globals}

# --- Serialized Data ---
${serialized_data}

# --- Functions ---
${functions}

# --- Node execution functions ---
${nodes_exec_func}

# --- Node dataclass Types with just an execute function (calls a node execution function above) ---
# The dataclass attributes are the node properties of type WrappedPropertyDescriptor in cls.__dict__.
${node_types}

""")


def generate_nodes_py(filename: str = 'nodes'):
    ''' Generates the nodes.py file in the root directory of your addon.

        Arguments:
        - 'filename': filename of the generated file, relative to the addon root directory.
    '''

    output_filepath: Path = GLOBALS.ADDON_SOURCE_PATH / f'{filename}.py'

    print(f"Searching for NodeExec subclasses....")

    # --- Helper to find all subclasses recursively --- 
    def find_subclasses_recursive(cls):
        direct = cls.__subclasses__()
        all_subs = set(direct)
        for d in direct:
            all_subs.update(find_subclasses_recursive(d))
        return all_subs

    # --- Find NodeExec subclasses after importing all modules --- 
    all_subclasses = find_subclasses_recursive(NodeExec)

    # --- Filter for final subclasses (no further subclasses) --- 
    final_subclasses = [sub for sub in all_subclasses if not sub.__subclasses__()]
    print(f"Found {len(final_subclasses)} final NodeExec subclasses.")

    node_type_definitions = []
    node_exec_func_definitions = []
    imports_set = set()
    globals_list = [] # You might want to add logic to populate these
    serialized_data_list = []
    functions_list = []

    # --- Helper to extract execute method source --- 
    def get_execute_source(cls):
        try:
            execute_method = cls.execute
            # Check if the execute method is directly defined in this class (not inherited from NodeExec)
            if execute_method.__qualname__.startswith(cls.__name__):
                source_lines, start_line = inspect.getsourcelines(execute_method)
                # Dedent the source code
                dedented_lines = inspect.cleandoc("\n".join(source_lines))
                # Parse the function definition to get args and body
                tree = ast.parse(dedented_lines)
                func_def = tree.body[0]
                if isinstance(func_def, ast.FunctionDef):
                    # Extract argument names (excluding self)
                    args = [arg.arg for arg in func_def.args.args if arg.arg != 'self']
                    # Extract the body, preserving indentation (relative to the function def)
                    body_lines = dedented_lines.split('\n')[1:] # Skip the def line
                    # Find the indentation of the first line of the body
                    first_line_indent = len(body_lines[0]) - len(body_lines[0].lstrip(' '))
                    # Re-indent the body lines
                    body = '\n'.join(['    ' + line[first_line_indent:] for line in body_lines])
                    return {'args': ', '.join(args), 'body': body}
        except (TypeError, OSError, IndexError, AttributeError) as e:
            print(f"Warning: Could not get source for execute in {cls.__name__}: {e}")
            pass # Method might not be defined or source unavailable
        return None

    # --- Helper to extract WrappedPropertyDescriptor fields --- 
    def get_wrapped_properties(cls):
        fields = []
        try:
            source_lines, _ = inspect.getsourcelines(cls)
            source_code = "".join(source_lines)
            tree = ast.parse(source_code)
            class_def = tree.body[0]
            if isinstance(class_def, ast.ClassDef):
                for node in class_def.body:
                    # Look for assignments like: my_prop: WPT.Float = WPT.Float(...)
                    if isinstance(node, ast.AnnAssign):
                        if isinstance(node.annotation, ast.Attribute) and isinstance(node.annotation.value, ast.Name) and node.annotation.value.id == 'WPT': # Assuming WPT alias for WrappedTypedPropertyTypes
                            target_name = node.target.id
                            # Try to reconstruct the assignment string (basic attempt)
                            # This is complex and might not be perfect
                            value_source = ast.unparse(node.value) if node.value else 'None'
                            annotation_source = ast.unparse(node.annotation)
                            fields.append(f"    {target_name}: {annotation_source} = {value_source}")
                        elif isinstance(node.annotation, ast.Name) and node.annotation.id == 'WrappedPropertyDescriptor': # Direct use
                             target_name = node.target.id
                             value_source = ast.unparse(node.value) if node.value else 'None'
                             annotation_source = ast.unparse(node.annotation)
                             fields.append(f"    {target_name}: {annotation_source} = {value_source}")
                    # Look for simple assignments: my_prop = WPT.Float(...)
                    elif isinstance(node, ast.Assign):
                         if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                             target_name = node.targets[0].id
                             # Check if the value is a call to WPT method or WrappedPropertyDescriptor
                             is_wpt_call = False
                             if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                                 if isinstance(node.value.func.value, ast.Name) and node.value.func.value.id == 'WPT':
                                     is_wpt_call = True
                             elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                                  if node.value.func.id == 'WrappedPropertyDescriptor':
                                      is_wpt_call = True # Or WPD directly

                             if is_wpt_call:
                                 value_source = ast.unparse(node.value)
                                 # Attempt to get annotation if available separately (less common for simple assign)
                                 annotation = getattr(cls, '__annotations__', {}).get(target_name)
                                 annotation_source = str(annotation) if annotation else 'Any' # Fallback annotation
                                 fields.append(f"    {target_name}: {annotation_source} = {value_source}")

        except (TypeError, OSError, AttributeError) as e:
             print(f"Warning: Could not parse source for fields in {cls.__name__}: {e}")
        return '\n'.join(fields) if fields else '    pass # No WrappedPropertyDescriptor fields found or parse error'


    for subclass in final_subclasses:
        node_type_name = subclass.__name__ + 'Data'
        print(f"  Processing: {subclass.__name__} -> {node_type_name}")

        # Extract fields
        fields_str = get_wrapped_properties(subclass)

        # Extract execute method
        exec_info = get_execute_source(subclass)
        exec_func_str = ''
        if exec_info:
            exec_func_template = TEMPLATE_NODE_EXEC_FUNC
            exec_func_str = exec_func_template.safe_substitute(
                args=exec_info['args'],
                body=exec_info['body']
            )
            # Indent the generated execute function
            exec_func_str = '\n'.join(['    ' + line for line in exec_func_str.split('\n')])
        else:
             exec_func_str = '    def execute(self, *args, **kwargs):\n        # Original class did not override execute\n        pass'

        # Generate dataclass definition
        node_type_template = TEMPLATE_NODE_TYPE
        node_type_def = node_type_template.safe_substitute(
            node_type_name=node_type_name,
            fields=fields_str,
            exec_func=exec_func_str
        )
        node_type_definitions.append(node_type_def)

        # Add imports from the original module if possible (basic)
        imports_set.add(f"from {subclass.__module__} import {subclass.__name__}")

    # --- Assemble the final script --- 
    script_content = SCRIPT_TEMPLATE.safe_substitute(
        imports='\n'.join(sorted(list(imports_set))),
        globals='\n'.join(globals_list),
        serialized_data='\n'.join(serialized_data_list),
        functions='\n'.join(functions_list),
        nodes_exec_func='\n\n'.join(node_exec_func_definitions), # Assuming separate exec funcs might be generated later
        node_types='\n\n'.join(node_type_definitions)
    )

    # --- Write to file --- 
    try:
        with open(output_filepath, 'w') as f:
            f.write("# --- Auto-generated Script by ackit.auto_code.nodes --- \n")
            f.write("# --- Edits will be overwritten! --- \n\n")
            # Add necessary imports for dataclasses and WrappedPropertyDescriptor
            f.write("from dataclasses import dataclass\n")
            f.write("from typing import Any, Set # Add other common types if needed\n")
            # Assuming WrappedTypedPropertyTypes is accessible, adjust if necessary
            f.write("from ackit.data.props_typed import WrappedTypedPropertyTypes as WPT, WrappedPropertyDescriptor\n")
            f.write("from ackit.ne.btypes.node_exec import NodeExec # Base class for generated dataclasses\n\n")
            f.write(script_content)
        print(f"Successfully generated {output_filepath}")
    except IOError as e:
        print(f"Error writing to {output_filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during file writing: {e}")




