import ast
from pathlib import Path

import astor
from lionwebpython.language import Language, Concept
from lionwebpython.language.primitive_type import PrimitiveType

from pylasu.lionweb.utils import to_snake_case


def language_generation(click, language: Language, output, language_name: str):
    imports = [
        ast.Import(names=[ast.alias(name="os", asname=None)]),
        ast.ImportFrom(module="typing", names=[ast.alias(name="cast", asname=None)], level=0),
        ast.ImportFrom(module="lionwebpython.language", names=[ast.alias(name="Language", asname=None)], level=0),
        ast.ImportFrom(module="lionwebpython.lionweb_version", names=[ast.alias(name="LionWebVersion", asname=None)],
                       level=0),
        ast.ImportFrom(module="lionwebpython.serialization.serialization_provider",
                       names=[ast.alias(name="SerializationProvider", asname=None)], level=0),
        ast.ImportFrom(module="pylasu.lionweb.starlasu", names=[ast.alias(name="position_deserializer", asname=None)],
                       level=0),
    ]
    load_starlasu_func = ast.FunctionDef(
        name="_load_starlasu",
        args=ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None,
                           defaults=[]),
        body=[
            ast.Assign(
                targets=[ast.Name(id="script_dir", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="os", ctx=ast.Load()),
                        attr="path.dirname",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="os", ctx=ast.Load()),
                                attr="path.abspath",
                                ctx=ast.Load()
                            ),
                            args=[ast.Name(id="__file__", ctx=ast.Load())],
                            keywords=[]
                        )
                    ],
                    keywords=[]
                )
            ),
            ast.Assign(
                targets=[ast.Name(id="jsonser", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="SerializationProvider", ctx=ast.Load()),
                        attr="get_standard_json_serialization",
                        ctx=ast.Load()
                    ),
                    args=[ast.Attribute(
                        value=ast.Name(id="LionWebVersion", ctx=ast.Load()),
                        attr="V2023_1",
                        ctx=ast.Load()
                    )],
                    keywords=[]
                )
            ),
            ast.Expr(value=ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="jsonser", ctx=ast.Load()),
                        attr="primitive_values_serialization",
                        ctx=ast.Load()
                    ),
                    attr="register_deserializer",
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value="com-strumenta-StarLasu-Position-id"),
                    ast.Name(id="position_deserializer", ctx=ast.Load())
                ],
                keywords=[]
            )),
            ast.Assign(
                targets=[ast.Name(id="starlasu_language_path", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="os", ctx=ast.Load()),
                        attr="path.join",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Name(id="script_dir", ctx=ast.Load()),
                        ast.Constant(value="starlasu.language.json")
                    ],
                    keywords=[]
                )
            ),
            ast.With(
                items=[ast.withitem(
                    context_expr=ast.Call(
                        func=ast.Name(id="open", ctx=ast.Load()),
                        args=[
                            ast.Name(id="starlasu_language_path", ctx=ast.Load()),
                            ast.Constant(value="r")
                        ],
                        keywords=[ast.keyword(arg="encoding", value=ast.Constant(value="utf-8"))]
                    ),
                    optional_vars=ast.Name(id="f", ctx=ast.Store())
                )],
                body=[
                    ast.Assign(
                        targets=[ast.Name(id="contents", ctx=ast.Store())],
                        value=ast.Call(
                            func=ast.Attribute(value=ast.Name(id="f", ctx=ast.Load()), attr="read", ctx=ast.Load()),
                            args=[], keywords=[]
                        )
                    )
                ]
            ),
            ast.Assign(
                targets=[ast.Name(id="starlasu_language", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="cast", ctx=ast.Load()),
                    args=[
                        ast.Name(id="Language", ctx=ast.Load()),
                        ast.Subscript(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="jsonser", ctx=ast.Load()),
                                    attr="deserialize_string_to_nodes",
                                    ctx=ast.Load()
                                ),
                                args=[ast.Name(id="contents", ctx=ast.Load())],
                                keywords=[]
                            ),
                            slice=ast.Constant(value=0),
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[]
                )
            ),
            ast.Return(value=ast.Name(id="starlasu_language", ctx=ast.Load()))
        ],
        decorator_list=[],
        returns=ast.Name(id="Language", ctx=ast.Load())
    )
    starlasu_assign = ast.Assign(
        targets=[ast.Name(id="STARLASU_LANGUAGE", ctx=ast.Store())],
        value=ast.Call(func=ast.Name(id="_load_starlasu", ctx=ast.Load()), args=[], keywords=[])
    )
    load_language_func = ast.FunctionDef(
        name="_load_language",
        args=ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None,
                           defaults=[]),
        body=[
            # script_dir = os.path.dirname(os.path.abspath(__file__))
            ast.Assign(
                targets=[ast.Name(id="script_dir", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="os", ctx=ast.Load()),
                        attr="path.dirname",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="os", ctx=ast.Load()),
                                attr="path.abspath",
                                ctx=ast.Load()
                            ),
                            args=[ast.Name(id="__file__", ctx=ast.Load())],
                            keywords=[]
                        )
                    ],
                    keywords=[]
                )
            ),
            # jsonser = SerializationProvider.get_standard_json_serialization(LionWebVersion.V2023_1)
            ast.Assign(
                targets=[ast.Name(id="jsonser", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="SerializationProvider", ctx=ast.Load()),
                        attr="get_standard_json_serialization",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Attribute(
                            value=ast.Name(id="LionWebVersion", ctx=ast.Load()),
                            attr="V2023_1",
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[]
                )
            ),
            # jsonser.primitive_values_serialization.register_deserializer(...)
            ast.Expr(value=ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="jsonser", ctx=ast.Load()),
                        attr="primitive_values_serialization",
                        ctx=ast.Load()
                    ),
                    attr="register_deserializer",
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value="com-strumenta-StarLasu-Position-id"),
                    ast.Name(id="position_deserializer", ctx=ast.Load())
                ],
                keywords=[]
            )),
            # jsonser.register_language(STARLASU_LANGUAGE)
            ast.Expr(value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="jsonser", ctx=ast.Load()),
                    attr="register_language",
                    ctx=ast.Load()
                ),
                args=[ast.Name(id="STARLASU_LANGUAGE", ctx=ast.Load())],
                keywords=[]
            )),
            # jsonser.instance_resolver.add_tree(STARLASU_LANGUAGE)
            ast.Expr(value=ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="jsonser", ctx=ast.Load()),
                        attr="instance_resolver",
                        ctx=ast.Load()
                    ),
                    attr="add_tree",
                    ctx=ast.Load()
                ),
                args=[ast.Name(id="STARLASU_LANGUAGE", ctx=ast.Load())],
                keywords=[]
            )),
            # rpg_language_path = os.path.join(script_dir, "rpg.language.json")
            ast.Assign(
                targets=[ast.Name(id="rpg_language_path", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="os", ctx=ast.Load()),
                        attr="path.join",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Name(id="script_dir", ctx=ast.Load()),
                        ast.Constant(value=f"{language_name.lower()}.language.json")
                    ],
                    keywords=[]
                )
            ),
            # with open(...) as f:
            ast.With(
                items=[ast.withitem(
                    context_expr=ast.Call(
                        func=ast.Name(id="open", ctx=ast.Load()),
                        args=[
                            ast.Name(id=f"{language_name.lower()}_language_path", ctx=ast.Load()),
                            ast.Constant(value="r")
                        ],
                        keywords=[ast.keyword(arg="encoding", value=ast.Constant(value="utf-8"))]
                    ),
                    optional_vars=ast.Name(id="f", ctx=ast.Store())
                )],
                body=[
                    ast.Assign(
                        targets=[ast.Name(id="contents", ctx=ast.Store())],
                        value=ast.Call(
                            func=ast.Attribute(value=ast.Name(id="f", ctx=ast.Load()), attr="read", ctx=ast.Load()),
                            args=[], keywords=[]
                        )
                    )
                ]
            ),
            # rpg_language = cast(Language, jsonser.deserialize_string_to_nodes(contents)[0])
            ast.Assign(
                targets=[ast.Name(id=f"{language_name.lower()}_language", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="cast", ctx=ast.Load()),
                    args=[
                        ast.Name(id="Language", ctx=ast.Load()),
                        ast.Subscript(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="jsonser", ctx=ast.Load()),
                                    attr="deserialize_string_to_nodes",
                                    ctx=ast.Load()
                                ),
                                args=[ast.Name(id="contents", ctx=ast.Load())],
                                keywords=[]
                            ),
                            slice=ast.Constant(value=0),
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[]
                )
            ),
            # return rpg_language
            ast.Return(value=ast.Name(id=f"{language_name.lower()}_language", ctx=ast.Load()))
        ],
        decorator_list=[],
        returns=ast.Name(id="Language", ctx=ast.Load())
    )
    language_assign = ast.Assign(
        targets=[ast.Name(id="LANGUAGE", ctx=ast.Store())],
        value=ast.Call(func=ast.Name(id="_load_language", ctx=ast.Load()), args=[], keywords=[])
    )

    module = ast.Module(
        body=imports + [
            load_starlasu_func,
            starlasu_assign,
            load_language_func,
            language_assign
        ],
        type_ignores=[]
    )

    for element in language.get_elements():
        if isinstance(element, Concept):
            assign = ast.Assign(
                targets=[ast.Name(id=to_snake_case(element.get_name()).upper(), ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="LANGUAGE", ctx=ast.Load()),
                        attr="get_concept_by_name",
                        ctx=ast.Load()
                    ),
                    args=[ast.Constant(value=element.get_name())],
                    keywords=[]
                )
            )
            module.body.append(assign)
        if isinstance(element, PrimitiveType):
            assign = ast.Assign(
                targets=[ast.Name(id=to_snake_case(element.get_name()).upper(), ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="LANGUAGE", ctx=ast.Load()),
                        attr="get_primitive_type_by_name",
                        ctx=ast.Load()
                    ),
                    args=[ast.Constant(value=element.get_name())],
                    keywords=[]
                )
            )
            module.body.append(assign)

    generated_code = astor.to_source(module)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    click.echo(f"📂 Saving language to: {output}")
    with Path(f"{output}/language.py").open("w", encoding="utf-8") as f:
        f.write(generated_code)
