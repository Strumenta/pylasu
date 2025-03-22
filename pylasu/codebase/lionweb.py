import base64
import re
from typing import Optional

from lionwebpython.language import Language, Concept, Property, Containment
from lionwebpython.language.classifier import Classifier
from lionwebpython.language.lioncore_builtins import LionCoreBuiltins
from lionwebpython.model.classifier_instance_utils import ClassifierInstanceUtils
from lionwebpython.model.impl.dynamic_node import DynamicNode
from lionwebpython.model.node import Node
from lionwebpython.lionweb_version import LionWebVersion
from lionwebpython.serialization.json_serialization import JsonSerialization

LW_REFERENCE_VERSION = LionWebVersion.V2023_1

CODEBASE_LANGUAGE = Language(lion_web_version=LW_REFERENCE_VERSION, name="Codebase",
                             id="strumenta-codebase", version="1", key="strumenta-codebase")

CODEBASE_FILE = Concept(lion_web_version=LW_REFERENCE_VERSION, name="CodebaseFile",
                        id="strumenta-codebase-file", key="strumenta-codebase-file")
CODEBASE_LANGUAGE.add_element(CODEBASE_FILE)

CODEBASE_FILE_LANGUAGE_NAME = Property(lion_web_version=LW_REFERENCE_VERSION, name="language_name",
                        id="strumenta-codebase-file-language-name")
CODEBASE_FILE.add_feature(CODEBASE_FILE_LANGUAGE_NAME)
CODEBASE_FILE_LANGUAGE_NAME.set_key("strumenta-codebase-file-language-name")
CODEBASE_FILE_LANGUAGE_NAME.set_optional(False)
CODEBASE_FILE_LANGUAGE_NAME.set_type(LionCoreBuiltins.get_string(LW_REFERENCE_VERSION))

CODEBASE_FILE_RELATIVE_PATH = Property(lion_web_version=LW_REFERENCE_VERSION, name="relative_path",
                        id="strumenta-codebase-file-relative-path")
CODEBASE_FILE.add_feature(CODEBASE_FILE_RELATIVE_PATH)
CODEBASE_FILE_RELATIVE_PATH.set_key("strumenta-codebase-file-relative-path")
CODEBASE_FILE_RELATIVE_PATH.set_optional(False)
CODEBASE_FILE_RELATIVE_PATH.set_type(LionCoreBuiltins.get_string(LW_REFERENCE_VERSION))

CODEBASE_FILE_CODE = Property(lion_web_version=LW_REFERENCE_VERSION, name="code",
                        id="strumenta-codebase-file-code")
CODEBASE_FILE.add_feature(CODEBASE_FILE_CODE)
CODEBASE_FILE_CODE.set_key("strumenta-codebase-file-code")
CODEBASE_FILE_CODE.set_optional(False)
CODEBASE_FILE_CODE.set_type(LionCoreBuiltins.get_string(LW_REFERENCE_VERSION))

CODEBASE_FILE_AST = Containment(lion_web_version=LW_REFERENCE_VERSION, name="ast",
                        id="strumenta-codebase-file-ast")
CODEBASE_FILE.add_feature(CODEBASE_FILE_AST)
CODEBASE_FILE_AST.set_key("strumenta-codebase-file-ast")
CODEBASE_FILE_AST.set_optional(True)
CODEBASE_FILE_AST.set_multiple(False)
CODEBASE_FILE_AST.set_type(LionCoreBuiltins.get_node(LW_REFERENCE_VERSION))


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

class CodebaseFile(DynamicNode):
    language_name: str
    relative_path: str
    code: str
    ast: Optional[Node]

    @property
    def language_name(self):
        return ClassifierInstanceUtils.get_property_value_by_name(self, 'language_name')

    @language_name.setter
    def language_name(self, value):
        ClassifierInstanceUtils.set_property_value_by_name(self, 'language_name', value)

    @property
    def relative_path(self):
        return ClassifierInstanceUtils.get_property_value_by_name(self, 'relative_path')

    @relative_path.setter
    def relative_path(self, value):
        ClassifierInstanceUtils.set_property_value_by_name(self, 'relative_path', value)

    @property
    def code(self):
        return ClassifierInstanceUtils.get_property_value_by_name(self, 'code')

    @code.setter
    def code(self, value):
        ClassifierInstanceUtils.set_property_value_by_name(self, 'code', value)

    @property
    def ast(self):
        containment = self.get_classifier().get_containment_by_name('ast')
        children = self.get_children(containment=containment)
        if len(children) == 0:
            return None
        else:
            return children[0]

    @ast.setter
    def ast(self, value):
        containment = self.get_classifier().get_containment_by_name('ast')
        children = self.get_children(containment=containment)
        if value is None:
            if len(children) != 0:
                self.remove_child(child=children[0])
        else:
            if len(children) != 0:
                self.remove_child(child=children[0])
            self.add_child(containment=containment, child=value)

    def __init__(self, language_name: str, relative_path: str, code: str, ast: Optional[Node] = None, id: Optional[str] = None):
        super().__init__(id or f"codebase_file_{to_lionweb_identifier(relative_path)}", CODEBASE_FILE)
        self.language_name = language_name
        self.relative_path = relative_path
        self.code = code
        self.ast = ast


def codebase_deserializer(classifier, serialized_instance,
    deserialized_instances_by_id, properties_values) -> CodebaseFile:
    language_name = properties_values[classifier.get_property_by_name('language_name')]
    relative_path = properties_values[classifier.get_property_by_name('relative_path')]
    code = properties_values[classifier.get_property_by_name('code')]
    return CodebaseFile(language_name=language_name, relative_path=relative_path, code=code, id=serialized_instance.id)


def register_codebase_deserializers(jsonser: JsonSerialization):
    jsonser.instantiator.register_custom_deserializer(CODEBASE_FILE.get_id(), codebase_deserializer)