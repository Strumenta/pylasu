import contextlib

from pylasu.model.naming import ReferenceByName
from pylasu.model.position import Point, Position
from pylasu.validation.validation import Result, Issue, IssueType, IssueSeverity
from deprecated import deprecated


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_result(json_result, root_unserializer) -> Result:
    result = Result(root=root_unserializer(json_result['root']) if 'root' in json_result else None)
    result.issues = [unserialize_issue(issue) for issue in json_result['issues']] if 'issues' in json_result else []
    return result


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_issue(json_issue) -> Issue:
    return Issue(
        type=unserialize_issue_type(json_issue['type']) if json_issue['type'] else None,
        message=json_issue['message'] if json_issue['message'] else None,
        severity=unserialize_issue_severity(json_issue['severity']) if json_issue['severity'] else None,
        position=unserialize_position(json_issue['position']) if json_issue['position'] else None
    )


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_issue_type(json_issue_type) -> IssueType or None:
    with contextlib.suppress(Exception):
        return IssueType[json_issue_type]


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_issue_severity(json_issue_severity) -> IssueSeverity:
    with contextlib.suppress(Exception):
        return IssueSeverity[json_issue_severity]


@deprecated(reason="Use LionWeb serialization instead")
def check_type(json, expected_type):
    if "#type" not in json:
        raise Exception("type not specified, expected %s" % expected_type)
    if json["#type"] != expected_type:
        raise Exception("unexpected type, expected %s but found %s" % (expected_type, json["#type"]))


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_point(json_point):
    return Point(
        line=json_point['line'] if 'line' in json_point else None,
        column=json_point['column'] if 'column' in json_point else None,
    )


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_position(json_position):
    return Position(
        start=unserialize_point(json_position['start']) if 'start' in json_position else None,
        end=unserialize_point(json_position['end']) if 'end' in json_position else None
    )


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_reference_by_name(json_reference_by_name):
    return ReferenceByName(
        name=json_reference_by_name['name'] if 'name' in json_reference_by_name else None
    )


@deprecated(reason="Use LionWeb serialization instead")
def unserialize_long(json):
    return json
