import ast
import keyword
from pathlib import Path
from typing import List, Dict

import astor
from lionwebpython.language import Language, Concept, Interface, Containment, Property
from lionwebpython.language.classifier import Classifier
from lionwebpython.language.enumeration import Enumeration
from lionwebpython.language.primitive_type import PrimitiveType
from lionwebpython.language.reference import Reference
from lionwebpython.lionweb_version import LionWebVersion

from pylasu.lionweb.starlasu import StarLasuBaseLanguage
from pylasu.lionweb.utils import to_snake_case


def make_cond(enumeration_name: str, member_name: str):
    return ast.Compare(
        left=ast.Name(id="serialized", ctx=ast.Load()),
        ops=[ast.Eq()],
        comparators=[
            ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id=enumeration_name, ctx=ast.Load()),
                    attr=member_name,
                    ctx=ast.Load()
                ),
                attr="value",
                ctx=ast.Load()
            )
        ]
    )

# The return: return AssignmentType.Add
def make_return(enumeration_name: str, member_name: str):
    return ast.Return(
        value=ast.Attribute(
            value=ast.Name(id=enumeration_name, ctx=ast.Load()),
            attr=member_name,
            ctx=ast.Load()
        )
    )


def deserializer_generation(click, language: Language, output):
    import_abc = ast.ImportFrom(
        module='abc',
        names=[ast.alias(name='ABC', asname=None)],
        level=0
    )
    import_dataclass = ast.ImportFrom(
        module='dataclasses',
        names=[ast.alias(name='dataclass', asname=None)],
        level=0
    )
    import_enum = ast.ImportFrom(
        module="enum",
        names=[ast.alias(name="Enum", asname=None)],
        level=0
    )
    import_typing = ast.ImportFrom(
        module='typing',
        names=[ast.alias(name='Optional', asname=None)],
        level=0
    )
    import_starlasu = ast.ImportFrom(
        module='pylasu.model.metamodel',
        names=[ast.alias(name='Expression', asname='StarLasuExpression'),
               ast.alias(name='PlaceholderElement', asname='StarLasuPlaceholderElement'),
               ast.alias(name='Named', asname='StarLasuNamed'),
               ast.alias(name='TypeAnnotation', asname='StarLasuTypeAnnotation'),
               ast.alias(name='Parameter', asname='StarLasuParameter'),
               ast.alias(name='Statement', asname='StarLasuStatement'),
               ast.alias(name='EntityDeclaration', asname='StarLasuEntityDeclaration'),
               ast.alias(name='BehaviorDeclaration', asname='StarLasuBehaviorDeclaration'),
               ast.alias(name='Documentation', asname='StarLasuDocumentation')],
        level=0
    )
    import_node = ast.ImportFrom(
        module='pylasu.model',
        names=[ast.alias(name='Node', asname=None)],
        level=0
    )
    import_ast = ast.ImportFrom(
        module='ast',
        names=[ast.alias(name=e.get_name(), asname=None) for e in language.get_elements() if not isinstance(e, PrimitiveType)],
        level=0
    )
    import_primitives = ast.ImportFrom(
        module='primitive_types',
        names=[ast.alias(name=e.get_name(), asname=None) for e in language.get_elements() if isinstance(e, PrimitiveType)],
        level=0
    )
    module = ast.Module(body=[import_abc, import_dataclass, import_typing, import_enum, import_starlasu, import_node,
                              import_ast, import_primitives],
                        type_ignores=[])



    for e in language.get_elements():
        if isinstance(e, Enumeration):
            arg_serialized = ast.arg(arg="serialized", annotation=ast.Name(id="str", ctx=ast.Load()))
            # The raise: raise ValueError(f"...")
            raise_stmt = ast.Raise(
                exc=ast.Call(
                    func=ast.Name(id="ValueError", ctx=ast.Load()),
                    args=[
                        ast.JoinedStr(values=[
                            ast.Constant(value=f"Invalid value for {e.get_name()}: "),
                            ast.FormattedValue(
                                value=ast.Name(id="serialized", ctx=ast.Load()),
                                conversion=-1
                            )
                        ])
                    ],
                    keywords=[]
                ),
                cause=None
            )
            # The function body
            literals = e.get_literals()
            current_if = ast.If(
                test=make_cond(e.get_name(), literals[0].get_name()),
                body=[make_return(e.get_name(), literals[0].get_name())],
                orelse=[]
            )
            root_if = current_if

            for literal in literals[1:]:
                next_if = ast.If(
                    test=make_cond(e.get_name(), literal.get_name()),
                    body=[make_return(e.get_name(), literal.get_name())],
                    orelse=[]
                )
                current_if.orelse = [next_if]
                current_if = next_if

            # Final else
            current_if.orelse = [raise_stmt]

            # Function definition
            func_def = ast.FunctionDef(
                name=f"_deserialize_{to_snake_case(e.get_name())}",
                args=ast.arguments(
                    posonlyargs=[],
                    args=[arg_serialized],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]
                ),
                body=[root_if],
                decorator_list=[],
                returns=ast.Constant(value=e.get_name())
            )
            module.body.append(func_def)

    generated_code = astor.to_source(module)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    click.echo(f"📂 Saving deserializer to: {output}")
    with Path(f"{output}/deserializer.py").open("w", encoding="utf-8") as f:
        f.write(generated_code)