import ast
from pathlib import Path
from typing import cast, List, Dict

import astor  # Install with `pip install astor`
import click
from lionwebpython.language import Language, Concept, Interface
from lionwebpython.language.enumeration import Enumeration
from lionwebpython.language.primitive_type import PrimitiveType
from lionwebpython.lionweb_version import LionWebVersion
from lionwebpython.serialization.serialization_provider import SerializationProvider

from pylasu.lionweb.starlasu import StarLasuBaseLanguage


def topological_concepts_sort(concepts: List[Concept]) -> List[Concept]:
    id_to_concept = {el.get_id(): el for el in concepts}

    # Build graph edges: child -> [parents]
    graph: Dict[str, List[str]] = {el.get_id(): [] for el in concepts}
    for el in concepts:
        if el.get_extended_concept() and el.get_extended_concept().get_id() in id_to_concept:
            graph[el.get_id()].append(el.get_extended_concept().get_id())

    visited = set()
    sorted_list = []

    def visit(name: str):
        if name in visited:
            return
        visited.add(name)
        for dep in graph[name]:
            visit(dep)
        sorted_list.append(id_to_concept[name])

    for el in concepts:
        visit(el.get_id())

    return sorted_list

@click.command()
@click.argument("dependencies", nargs=-1, type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument("lionweb-language", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument("output", type=click.Path(exists=False, file_okay=False, writable=True))
def main(dependencies, lionweb_language, output):
    """Simple CLI that processes a file and writes results to a directory."""
    serialization = SerializationProvider.get_standard_json_serialization(LionWebVersion.V2023_1)

    for dep in dependencies:
        click.echo(f"Processing dependency {dep}")
        with open(dep, "r", encoding="utf-8") as f:
            content = f.read()
            language = cast(Language, serialization.deserialize_string_to_nodes(content)[0])
            serialization.register_language(language=language)
            serialization.classifier_resolver.register_language(language)
            serialization.instance_resolver.add_tree(language)

    click.echo(f"📄 Processing file: {lionweb_language}")
    with open(lionweb_language, "r", encoding="utf-8") as f:
        content = f.read()
        language = cast(Language, serialization.deserialize_string_to_nodes(content)[0])

    import_abc = ast.ImportFrom(
        module='abc',
        names=[ast.alias(name='ABC', asname=None)],
        level=0
    )
    import_node = ast.ImportFrom(
        module='pylasu.model',
        names=[ast.alias(name='Node', asname=None)],
        level=0
    )
    module = ast.Module(body=[import_abc, import_node], type_ignores=[])


    for element in language.get_elements():
        if isinstance(element, Concept):
            pass
        elif isinstance(element, Interface):
            pass
        elif isinstance(element, PrimitiveType):
            pass
        elif isinstance(element, Enumeration):
            pass
        else:
            raise ValueError(f"Unsupported {element}")

    sorted_concepts = topological_concepts_sort([c for c in language.get_elements() if isinstance(c, Concept)])

    for concept in sorted_concepts:
        bases = []
        if concept.get_extended_concept().id == StarLasuBaseLanguage.get_astnode(LionWebVersion.V2023_1).id:
            bases.append('Node')
        else:
            bases.append(concept.get_extended_concept().get_name())
        if concept.is_abstract():
            bases.append('ABC')
        classdef = ast.ClassDef(concept.get_name(), bases=bases,
            keywords=[],
            body=[ast.Pass()],
            decorator_list=[])
        module.body.append(classdef)

    click.echo(f"📂 Saving results to: {output}")
    generated_code = astor.to_source(module)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    with Path(f"{output}/ast.py").open("w", encoding="utf-8") as f:
        f.write(generated_code)

if __name__ == "__main__":
    main()