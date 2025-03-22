import ast
import keyword
from _ast import ClassDef
from pathlib import Path
from typing import List, Dict

import astor
from lionwebpython.language import Language, Concept, Interface, Containment, Property, Feature
from lionwebpython.language.classifier import Classifier
from lionwebpython.language.enumeration import Enumeration
from lionwebpython.language.primitive_type import PrimitiveType
from lionwebpython.language.reference import Reference
from lionwebpython.lionweb_version import LionWebVersion

from pylasu.lionweb.starlasu import StarLasuBaseLanguage
from pylasu.lionweb.utils import calculate_field_name, to_snake_case


def _identify_topological_deps(classifiers: List[Classifier], id_to_concept) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = {el.get_id(): [] for el in classifiers}
    for c in classifiers:
        if isinstance(c, Concept):
            if c.get_extended_concept() and c.get_extended_concept().get_id() in id_to_concept:
                graph[c.get_id()].append(c.get_extended_concept().get_id())
            for i in c.get_implemented():
                graph[c.get_id()].append(i.get_id())
            for f in c.get_features():
                if isinstance(f, Containment):
                    if f.get_type() and f.get_type().get_id() in id_to_concept:
                        graph[c.get_id()].append(f.get_type().get_id())
        elif isinstance(c, Interface):
            pass
        else:
            raise ValueError()
    return graph


def topological_classifiers_sort(classifiers: List[Classifier]) -> List[Classifier]:
    id_to_concept = {el.get_id(): el for el in classifiers}

    # Build graph edges: child -> [parents]
    graph: Dict[str, List[str]] = _identify_topological_deps(classifiers, id_to_concept)

    visited = set()
    sorted_list = []

    def visit(name: str):
        if name in visited:
            return
        visited.add(name)
        if name in graph:
            for dep in graph[name]:
                visit(dep)
        if name in id_to_concept:
            sorted_list.append(id_to_concept[name])

    for c in classifiers:
        visit(c.get_id())

    return sorted_list


def _generate_from_containment(feature: Containment, classdef: ClassDef):
    field_name = calculate_field_name(feature)
    type = feature.get_type().get_name()
    if feature.is_multiple():
        type = f"List[{type}]"
    elif feature.is_optional():
        type = f"Optional[{type}]"
    field = ast.AnnAssign(
        target=ast.Name(id=field_name, ctx=ast.Store()),
        annotation=ast.Constant(value=type),
        value=None,
        simple=1,
    )
    if len(classdef.body) == 1 and isinstance(classdef.body[0], ast.Pass):
        classdef.body = []
    classdef.body.append(field)


def _generate_from_feature(feature: Feature, classdef: ClassDef):
    if isinstance(feature, Containment):
        _generate_from_containment(feature, classdef)
    elif isinstance(feature, Reference):
        field_name = feature.get_name()
        if field_name in keyword.kwlist:
            field_name = f"{field_name}_"
        type = f"ReferenceByName[{feature.get_type().get_name()}]"
        if feature.is_optional():
            type = f"Optional[{type}]"
        field = ast.AnnAssign(
            target=ast.Name(id=field_name, ctx=ast.Store()),
            annotation=ast.Constant(value=type),
            value=None,
            simple=1,
        )
        if len(classdef.body) == 1 and isinstance(classdef.body[0], ast.Pass):
            classdef.body = []
        classdef.body.append(field)
    elif isinstance(feature, Property):
        field_name = feature.get_name()
        if field_name in keyword.kwlist:
            field_name = f"{field_name}_"
        type = feature.get_type().get_name()
        if feature.is_optional():
            type = f"Optional[{type}]"
        field = ast.AnnAssign(
            target=ast.Name(id=field_name, ctx=ast.Store()),
            annotation=ast.Constant(value=type),
            value=None,
            simple=1,
        )
        if len(classdef.body) == 1 and isinstance(classdef.body[0], ast.Pass):
            classdef.body = []
        classdef.body.append(field)
    else:
        raise ValueError()


def _generate_constructor(concept: Concept) -> ast.FunctionDef:
    return ast.FunctionDef(
        name="__init__",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self", annotation=None),
                ast.arg(arg="id", annotation=ast.Name(id="str", ctx=ast.Load())),
                ast.arg(arg="position", annotation=ast.Subscript(
                    value=ast.Name(id="Optional", ctx=ast.Load()),
                    slice=ast.Name(id="Position", ctx=ast.Load()),
                    ctx=ast.Load()
                )),
            ],
            kwonlyargs=[], kw_defaults=[], defaults=[]
        ),
        body=[
            # super().__init__(id=id, position=position, concept=concept)
            ast.Expr(value=ast.Call(
                func=ast.Attribute(
                    value=ast.Call(func=ast.Name(id='super', ctx=ast.Load()), args=[], keywords=[]),
                    attr='__init__',
                    ctx=ast.Load()
                ),
                args=[],
                keywords=[
                    ast.keyword(arg='id', value=ast.Name(id='id', ctx=ast.Load())),
                    ast.keyword(arg='position', value=ast.Name(id='position', ctx=ast.Load())),
                    ast.keyword(arg='concept', value=ast.Name(id=ast.Name(id=to_snake_case(concept.get_name()).upper(), ctx=ast.Load()))),
                ]
            )),
            # self.set_id(id)
            ast.Expr(value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='set_id', ctx=ast.Load()),
                args=[ast.Name(id='id', ctx=ast.Load())],
                keywords=[]
            )),
            # # self._set_containment_single_value(..., ...)
            # ast.Expr(value=ast.Call(
            #     func=ast.Attribute(
            #         value=ast.Name(id='self', ctx=ast.Load()),
            #         attr='_set_containment_single_value',
            #         ctx=ast.Load()
            #     ),
            #     args=[],
            #     keywords=[
            #         ast.keyword(
            #             arg='containment',
            #             value=ast.Call(
            #                 func=ast.Attribute(
            #                     value=ast.Name(id='concept', ctx=ast.Load()),
            #                     attr='get_containment_by_name',
            #                     ctx=ast.Load()
            #                 ),
            #                 args=[ast.Constant(value='externalName')],
            #                 keywords=[]
            #             )
            #         ),
            #         ast.keyword(
            #             arg='value',
            #             value=ast.Name(id='externalName', ctx=ast.Load())
            #         )
            #     ]
            # ))
        ],
        decorator_list=[],
        returns=None
    )


def _generate_from_concept(classifier: Concept) -> ClassDef:
    bases = []
    if classifier.get_extended_concept().id == StarLasuBaseLanguage.get_astnode(LionWebVersion.V2023_1).id:
        if len(classifier.get_implemented()) == 0:
            bases.append('ASTNode')
    else:
        bases.append(classifier.get_extended_concept().get_name())
    special_interfaces = {
        'com-strumenta-StarLasu-Expression-id': 'StarLasuExpression',
        'com-strumenta-StarLasu-Statement-id': 'StarLasuStatement',
        'com-strumenta-StarLasu-PlaceholderElement-id': 'StarLasuPlaceholderElement',
        'com-strumenta-StarLasu-Parameter-id': 'StarLasuParameter',
        'com-strumenta-StarLasu-Documentation-id': 'StarLasuDocumentation',
        'com-strumenta-StarLasu-BehaviorDeclaration-id': 'StarLasuBehaviorDeclaration',
        'com-strumenta-StarLasu-EntityDeclaration-id': 'StarLasuEntityDeclaration',
        'com-strumenta-StarLasu-TypeAnnotation-id': 'StarLasuTypeAnnotation',
        'LionCore-builtins-INamed': 'StarLasuNamed'
    }
    for i in classifier.get_implemented():
        if i.get_id() in special_interfaces:
            bases.append(special_interfaces[i.get_id()])
        else:
            bases.append(i.get_name())
    # if classifier.is_abstract():
    #    bases.append('ABC')
    dataclass_decorator = ast.Name(id="dataclass", ctx=ast.Load())
    classdef = ast.ClassDef(classifier.get_name(), bases=bases,
                            keywords=[],
                            body=[],
                            decorator_list=[dataclass_decorator])

    for feature in classifier.get_features():
        _generate_from_feature(feature, classdef)

    classdef.body.append(_generate_constructor(classifier))

    return classdef


def ast_generation(click, language: Language, output, language_name=str):
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
        module='pylasu.lwmodel',
        names=[ast.alias(name='ASTNode', asname=None)],
        level=0
    )
    import_language = ast.ImportFrom(
        module='lionwebpython.language',
        names=[ast.alias(name='Concept', asname=None)],
        level=0
    )
    import_model = ast.ImportFrom(
        module='pylasu.model',
        names=[ast.alias(name='Position', asname=None)],
        level=0
    )
    # from rpg.language import CONTROL_SPECIFICATION
    import_concepts = ast.ImportFrom(
        module=f"{language_name.lower()}.language",
        names=[ast.alias(name=to_snake_case(e.get_name()).upper(), asname=None)for e in language.get_elements() if isinstance(e, Concept)],
        level=0
    )
    module = ast.Module(body=[import_abc, import_dataclass, import_typing, import_enum, import_starlasu, import_node,
                              import_language, import_model, import_concepts],
                        type_ignores=[])

    for element in language.get_elements():
        if isinstance(element, Concept):
            pass
        elif isinstance(element, Interface):
            pass
        elif isinstance(element, PrimitiveType):
            pass
        elif isinstance(element, Enumeration):
            members = [
                ast.Assign(
                    targets=[ast.Name(id=literal.get_name(), ctx=ast.Store())],
                    value=ast.Constant(value=literal.get_name())
                )
                for literal in element.get_literals()
            ]

            enum_class = ast.ClassDef(
                name=element.get_name(),
                bases=[ast.Name(id="Enum", ctx=ast.Load())],
                keywords=[],
                body=members,
                decorator_list=[]
            )
            module.body.append(enum_class)
        else:
            raise ValueError(f"Unsupported {element}")

    sorted_classifier = topological_classifiers_sort([c for c in language.get_elements() if isinstance(c, Classifier)])

    for classifier in sorted_classifier:
        if isinstance(classifier, Concept):
            module.body.append(_generate_from_concept(classifier))
        elif isinstance(classifier, Interface):
            bases = []
            if len(classifier.get_extended_interfaces()) == 0:
                bases.append("ASTNode")
                # bases.append("ABC")

            classdef = ast.ClassDef(classifier.get_name(), bases=bases,
                                    keywords=[],
                                    body=[ast.Pass()],
                                    decorator_list=[])
            module.body.append(classdef)
        else:
            raise ValueError()

    click.echo(f"📂 Saving ast to: {output}")
    generated_code = astor.to_source(module)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    with Path(f"{output}/ast.py").open("w", encoding="utf-8") as f:
        f.write(generated_code)
