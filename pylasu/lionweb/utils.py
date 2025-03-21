import re

def to_snake_case(name: str) -> str:
    # Replace capital letters with _lowercase, except at the beginning
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()