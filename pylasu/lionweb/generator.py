from typing import cast

import click
from language_generation import language_generation
from lionwebpython.language import Language
from lionwebpython.lionweb_version import LionWebVersion
from lionwebpython.serialization.serialization_provider import \
    SerializationProvider


@click.command()
@click.argument(
    "dependencies",
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.argument(
    "lionweb-language", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.argument("output", type=click.Path(exists=False, file_okay=False, writable=True))
@click.option("--language-name", required=True, type=str, help="Name of the language")
def main(dependencies, lionweb_language, output, language_name):
    from pylasu.lionweb.ast_generation import ast_generation
    from pylasu.lionweb.deserializer_generation import deserializer_generation

    """Simple CLI that processes a file and writes results to a directory."""
    serialization = SerializationProvider.get_standard_json_serialization(
        LionWebVersion.V2023_1
    )

    for dep in dependencies:
        click.echo(f"Processing dependency {dep}")
        with open(dep, "r", encoding="utf-8") as f:
            content = f.read()
            language = cast(
                Language, serialization.deserialize_string_to_nodes(content)[0]
            )
            serialization.register_language(language=language)
            serialization.classifier_resolver.register_language(language)
            serialization.instance_resolver.add_tree(language)

    click.echo(f"📄 Processing file: {lionweb_language}")
    with open(lionweb_language, "r", encoding="utf-8") as f:
        content = f.read()
        language = cast(Language, serialization.deserialize_string_to_nodes(content)[0])
    ast_generation(click, language, output, language_name)
    deserializer_generation(click, language, output)
    language_generation(click, language, output, language_name)


if __name__ == "__main__":
    main()
