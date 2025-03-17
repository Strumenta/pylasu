import ast
from pathlib import Path
from symtable import Class
from typing import cast

import astor  # Install with `pip install astor`
import click
import os
import sys

from lionwebpython.language import Language, Concept, Interface
from lionwebpython.language.classifier import Classifier
from lionwebpython.language.primitive_type import PrimitiveType
from lionwebpython.lionweb_version import LionWebVersion
from lionwebpython.serialization.serialization_provider import SerializationProvider

# Define the function AST
func_def = ast.FunctionDef(
    name="hello_world",
    args=ast.arguments(
        posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
    ),
    body=[
        ast.Expr(value=ast.Call(
            func=ast.Name(id="print", ctx=ast.Load()),
            args=[ast.Constant(value="Hello, world!")], keywords=[]
        ))
    ],
    decorator_list=[],
)

# # Convert AST to code
# module = ast.Module(body=[func_def], type_ignores=[])
# generated_code = astor.to_source(module)
#
# print(generated_code)
#

@click.command()
@click.argument("lionweb-language", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument("output", type=click.Path(exists=False, file_okay=False, writable=True))
def main(lionweb_language, output):
    """Simple CLI that processes a file and writes results to a directory."""
    serialization = SerializationProvider.get_standard_json_serialization(LionWebVersion.V2023_1)
    click.echo(f"📄 Processing file: {lionweb_language}")
    with open(lionweb_language, "r", encoding="utf-8") as f:
        content = f.read()
        language = cast(Language, serialization.deserialize_string_to_nodes(content)[0])

    module = ast.Module(body=[], type_ignores=[])
    for element in language.get_elements():
        if isinstance(element, Concept):
            classdef = ast.ClassDef(element.get_name(), bases=[],  # No parent classes
                keywords=[],
                body=[ast.Pass()],
                decorator_list=[])
            module.body.append(classdef)
        elif isinstance(element, Interface):
            pass
        elif isinstance(element, PrimitiveType):
            pass
        else:
            raise ValueError(f"Unsupported {element}")
    click.echo(f"📂 Saving results to: {output}")
    generated_code = astor.to_source(module)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    with Path(f"{output}/ast.py").open("w", encoding="utf-8") as f:
        f.write(generated_code)

if __name__ == "__main__":
    main()