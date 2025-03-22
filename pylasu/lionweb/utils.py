import keyword
import re

from lionwebpython.language import Feature
from lionwebpython.lionweb_version import LionWebVersion

LW_REFERENCE_VERSION = LionWebVersion.V2023_1


def to_snake_case(name: str) -> str:
    # Replace capital letters with _lowercase, except at the beginning
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def calculate_field_name(feature: Feature) -> str:
    field_name = feature.get_name()
    if field_name in keyword.kwlist:
        field_name = f"{field_name}_"
    return field_name


def to_lionweb_identifier(s: str) -> str:
    """
    Converts a given string into a valid LionWeb identifier.

    Rules:
    - Starts with a letter (a-z, A-Z) or underscore (_)
    - Only contains letters, digits (0-9), and underscores (_)
    - Replaces invalid characters with underscores (_)
    - Ensures the identifier does not start with a digit

    Args:
        s (str): Input string to be converted.

    Returns:
        str: Valid LionWeb identifier.
    """
    # Replace invalid characters with underscores
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)

    # Ensure it does not start with a digit by prefixing with "_"
    if s and s[0].isdigit():
        s = "_" + s

    # Ensure the identifier is not empty
    return s if s else "_"
