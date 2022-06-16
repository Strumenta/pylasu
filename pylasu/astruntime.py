from .kolasuast import ReferenceByName
from .model.position import Point, Position
from .validation.validation import Result


def unserialize_result(json, root_unserializer) -> Result:
    errors = []
    for json_error in json["errors"]:
        raise Exception()
    return Result(root_unserializer(json["root"]), errors)


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
