from dataclasses import dataclass

from .kolasuast import Point, Position, ASTNode, ReferenceByName


@dataclass
class Issue:
    pass


@dataclass
class ParsingResult:
    errors: [Issue]
    root: ASTNode


def unserialize_result(json, root_unserializer) -> ParsingResult:
    errors = []
    for json_error in json["errors"]:
        raise Exception()
    return ParsingResult(errors=errors, root=root_unserializer(json["root"]))


def check_type(json, expected_type):
    if "#type" not in json:
        raise Exception("type not specified, expected %s" % expected_type)
    if json["#type"] != expected_type:
        raise Exception("unexpected type, expected %s but found %s" % (expected_type, json["#type"]))


def unserialize_point(json):
    return Point(line=json["line"], column=json["column"])


def unserialize_position(json):
    return Position(start=unserialize_point(json["start"]), end=unserialize_point(json["end"]))


def unserialize_reference_by_name(json):
    return ReferenceByName(json["name"])


def unserialize_long(json):
    return json
