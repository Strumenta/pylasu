from lionwebpython.serialization.json_serialization import JsonSerialization

from pylasu.codebase.codebase_file import CodebaseFile


def _codebase_deserializer(
    classifier, serialized_instance, deserialized_instances_by_id, properties_values
) -> CodebaseFile:
    language_name = properties_values[classifier.get_property_by_name("language_name")]
    relative_path = properties_values[classifier.get_property_by_name("relative_path")]
    code = properties_values[classifier.get_property_by_name("code")]
    return CodebaseFile(
        language_name=language_name,
        relative_path=relative_path,
        code=code,
        id=serialized_instance.id,
    )


def register_codebase_deserializers(jsonser: JsonSerialization):
    from pylasu.codebase.lwlanguage import CODEBASE_FILE

    jsonser.instantiator.register_custom_deserializer(
        CODEBASE_FILE.get_id(), _codebase_deserializer
    )
