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
from pylasu.lionweb.utils import calculate_field_name


def topological_classifiers_sort(classifiers: List[Classifier]) -> List[Classifier]:
    id_to_concept = {el.get_id(): el for el in classifiers}

    # Build graph edges: child -> [parents]
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


def ast_generation(click, language: Language, output):
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
    module = ast.Module(body=[import_abc, import_dataclass, import_typing, import_enum, import_starlasu, import_node],
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
            bases = []
            if classifier.get_extended_concept().id == StarLasuBaseLanguage.get_astnode(LionWebVersion.V2023_1).id:
                if len(classifier.get_implemented()) == 0:
                    bases.append('Node')
            else:
                bases.append(classifier.get_extended_concept().get_name())
            for i in classifier.get_implemented():
                if i.get_id() == 'com-strumenta-StarLasu-Expression-id':
                    bases.append('StarLasuExpression')
                elif i.get_id() == 'com-strumenta-StarLasu-Statement-id':
                    bases.append('StarLasuStatement')
                elif i.get_id() == 'com-strumenta-StarLasu-PlaceholderElement-id':
                    bases.append('StarLasuPlaceholderElement')
                elif i.get_id() == 'com-strumenta-StarLasu-Parameter-id':
                    bases.append('StarLasuParameter')
                elif i.get_id() == 'com-strumenta-StarLasu-Documentation-id':
                    bases.append('StarLasuDocumentation')
                elif i.get_id() == 'com-strumenta-StarLasu-TypeAnnotation-id':
                    bases.append('StarLasuTypeAnnotation')
                elif i.get_id() == 'com-strumenta-StarLasu-BehaviorDeclaration-id':
                    bases.append('StarLasuBehaviorDeclaration')
                elif i.get_id() == 'com-strumenta-StarLasu-EntityDeclaration-id':
                    bases.append('StarLasuEntityDeclaration')
                elif i.get_id() == 'LionCore-builtins-INamed':
                    bases.append('StarLasuNamed')
                else:
                    bases.append(i.get_name())
            # if classifier.is_abstract():
            #    bases.append('ABC')
            dataclass_decorator = ast.Name(id="dataclass", ctx=ast.Load())
            classdef = ast.ClassDef(classifier.get_name(), bases=bases,
                                    keywords=[],
                                    body=[ast.Pass()],
                                    decorator_list=[dataclass_decorator])

            for feature in classifier.get_features():
                if isinstance(feature, Containment):
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

            module.body.append(classdef)
        elif isinstance(classifier, Interface):
            bases = []
            if len(classifier.get_extended_interfaces()) == 0:
                bases.append("Node")
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
