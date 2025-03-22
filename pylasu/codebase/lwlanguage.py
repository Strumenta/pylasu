from lionwebpython.language import Concept, Containment, Language, Property
from lionwebpython.language.lioncore_builtins import LionCoreBuiltins

from pylasu.lionweb.utils import LW_REFERENCE_VERSION

CODEBASE_LANGUAGE = Language(
    lion_web_version=LW_REFERENCE_VERSION,
    name="Codebase",
    id="strumenta-codebase",
    version="1",
    key="strumenta-codebase",
)

CODEBASE_FILE = Concept(
    lion_web_version=LW_REFERENCE_VERSION,
    name="CodebaseFile",
    id="strumenta-codebase-file",
    key="strumenta-codebase-file",
)
CODEBASE_LANGUAGE.add_element(CODEBASE_FILE)

CODEBASE_FILE_LANGUAGE_NAME = Property(
    lion_web_version=LW_REFERENCE_VERSION,
    name="language_name",
    id="strumenta-codebase-file-language-name",
)
CODEBASE_FILE.add_feature(CODEBASE_FILE_LANGUAGE_NAME)
CODEBASE_FILE_LANGUAGE_NAME.set_key("strumenta-codebase-file-language-name")
CODEBASE_FILE_LANGUAGE_NAME.set_optional(False)
CODEBASE_FILE_LANGUAGE_NAME.set_type(LionCoreBuiltins.get_string(LW_REFERENCE_VERSION))

CODEBASE_FILE_RELATIVE_PATH = Property(
    lion_web_version=LW_REFERENCE_VERSION,
    name="relative_path",
    id="strumenta-codebase-file-relative-path",
)
CODEBASE_FILE.add_feature(CODEBASE_FILE_RELATIVE_PATH)
CODEBASE_FILE_RELATIVE_PATH.set_key("strumenta-codebase-file-relative-path")
CODEBASE_FILE_RELATIVE_PATH.set_optional(False)
CODEBASE_FILE_RELATIVE_PATH.set_type(LionCoreBuiltins.get_string(LW_REFERENCE_VERSION))

CODEBASE_FILE_CODE = Property(
    lion_web_version=LW_REFERENCE_VERSION,
    name="code",
    id="strumenta-codebase-file-code",
)
CODEBASE_FILE.add_feature(CODEBASE_FILE_CODE)
CODEBASE_FILE_CODE.set_key("strumenta-codebase-file-code")
CODEBASE_FILE_CODE.set_optional(False)
CODEBASE_FILE_CODE.set_type(LionCoreBuiltins.get_string(LW_REFERENCE_VERSION))

CODEBASE_FILE_AST = Containment(
    lion_web_version=LW_REFERENCE_VERSION, name="ast", id="strumenta-codebase-file-ast"
)
CODEBASE_FILE.add_feature(CODEBASE_FILE_AST)
CODEBASE_FILE_AST.set_key("strumenta-codebase-file-ast")
CODEBASE_FILE_AST.set_optional(True)
CODEBASE_FILE_AST.set_multiple(False)
CODEBASE_FILE_AST.set_type(LionCoreBuiltins.get_node(LW_REFERENCE_VERSION))
