import unittest

from pylasu.model import Node


def assert_asts_are_equal(
        case: unittest.TestCase,
        expected: Node, actual: Node,
        context: str = "<root>", consider_position: bool = False
):
    if expected.node_type != actual.node_type:
        case.fail(f"{context}: expected node of type {expected.node_type}, "
                  f"but found {actual.node_type}")
    if consider_position:
        case.assertEqual(expected.position, actual.position, f"{context}.position")
    for expected_property in expected.properties:
        try:
            actual_property = next(filter(lambda p: p.name == expected_property.name, actual.properties))
        except StopIteration:
            case.fail(f"No property {expected_property.name} found at {context}")
        actual_prop_value = actual_property.value
        expected_prop_value = expected_property.value
        if expected_property.provides_nodes:
            if expected_property.multiple:
                assert_multi_properties_are_equal(
                    case, expected_property, expected_prop_value, actual_prop_value, context, consider_position)
            else:
                assert_single_properties_are_equal(case, expected_property, expected_prop_value, actual_prop_value,
                                                   context, consider_position)
        # TODO not yet supported elif expected_property.property_type == PropertyType.REFERENCE:
        else:
            case.assertEqual(
                expected_prop_value, actual_prop_value,
                f"{context}, comparing property {expected_property.name} of {expected.node_type}")


def assert_single_properties_are_equal(case, expected_property, expected_prop_value, actual_prop_value, context,
                                       consider_position):
    if expected_prop_value is None and actual_prop_value is not None:
        case.assertEqual(expected_prop_value, actual_prop_value,
                         f"{context}.{expected_property.name}")
    elif expected_prop_value is not None and actual_prop_value is None:
        case.assertEqual(expected_prop_value, actual_prop_value,
                         f"{context}.{expected_property.name}")
    elif expected_prop_value is None and actual_prop_value is None:
        # that is ok
        pass
    else:
        case.assertIsInstance(actual_prop_value, Node)
        assert_asts_are_equal(
            case, expected_prop_value, actual_prop_value,
            context=f"{context}.{expected_property.name}",
            consider_position=consider_position)


def assert_multi_properties_are_equal(case, expected_property, expected_prop_value, actual_prop_value, context,
                                      consider_position):
    # TODO IgnoreChildren
    case.assertEqual(actual_prop_value is None, expected_prop_value is None,
                     f"{context}.{expected_property.name} nullness")
    if actual_prop_value is not None and expected_prop_value is not None:
        case.assertEqual(len(actual_prop_value), len(expected_prop_value),
                         f"{context}.{expected_property.name} length")
    for expected_it, actual_it, i in \
            zip(expected_prop_value, actual_prop_value, range(len(expected_prop_value))):
        assert_asts_are_equal(case, expected_it, actual_it, f"{context}[{i}]",
                              consider_position=consider_position)
