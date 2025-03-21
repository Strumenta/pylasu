from typing import TYPE_CHECKING, Dict, Optional, cast

from lionwebpython.language import Language, Concept
from lionwebpython.language.lioncore_builtins import LionCoreBuiltins
from lionwebpython.language.primitive_type import PrimitiveType
from lionwebpython.lionweb_version import LionWebVersion

from pylasu.model import Point, Position


class StarLasuBaseLanguage(Language):
    if TYPE_CHECKING:
        from lionwebpython.language.concept import Concept
        from lionwebpython.language.interface import Interface
        from lionwebpython.language.primitive_type import PrimitiveType
        from lionwebpython.language.property import Property
        from lionwebpython.lionweb_version import LionWebVersion
        from lionwebpython.utils.id_utils import IdUtils

    _instances: Dict["LionWebVersion", "LionCoreBuiltins"] = {}

    def __init__(self, lion_web_version: "LionWebVersion"):
        super().__init__(lion_web_version=lion_web_version, name="com.strumenta.StarLasu")
        from lionwebpython.lionweb_version import LionWebVersion
        from lionwebpython.utils.id_utils import IdUtils

        version_id_suffix = (
            f"-{IdUtils.clean_string(lion_web_version.value)}"
            if lion_web_version != LionWebVersion.V2023_1
            else ""
        )

        if lion_web_version == LionWebVersion.V2023_1:
            version = "1"
        elif lion_web_version == LionWebVersion.V2024_1:
            version = "2"
        else:
            raise ValueError()

        self.set_id(f"com-strumenta-StarLasu{version_id_suffix}")
        self.set_key("com_strumenta_starlasu")
        self.set_version(version)

        self.char = PrimitiveType(lion_web_version=lion_web_version, language=self,
                                  name="Char", id=f"com-strumenta-StarLasu-Char-id{version_id_suffix}",
                                  key="com_strumenta_starlasu-Char-key")
        self.point = PrimitiveType(lion_web_version=lion_web_version, language=self,
                                  name="Point", id=f"com-strumenta-StarLasu-Point-id{version_id_suffix}",
                                  key="com_strumenta_starlasu-Point-key")
        self.position = PrimitiveType(lion_web_version=lion_web_version, language=self,
                                   name="Position", id=f"com-strumenta-StarLasu-Position-id{version_id_suffix}",
                                   key="com_strumenta_starlasu-Position-key")
        self.astnode = Concept(lion_web_version=lion_web_version, language=self,
                               name="ASTNode", key="com_strumenta_starlasu-ASTNode-key",
                               id="com-strumenta-StarLasu-ASTNode-id")

    @classmethod
    def get_astnode(
        cls, lion_web_version: LionWebVersion = LionWebVersion.current_version()
    ) -> "Concept":
        return cls.get_instance(lion_web_version).astnode

    @classmethod
    def get_instance(
        cls, lion_web_version: Optional["LionWebVersion"] = None
    ) -> "StarLasuBaseLanguage":
        if lion_web_version is None:
            from lionwebpython.lionweb_version import LionWebVersion

            lion_web_version = LionWebVersion.current_version()

        if lion_web_version not in cls._instances:
            cls._instances[lion_web_version] = StarLasuBaseLanguage(lion_web_version)

        return cls._instances[lion_web_version]

def position_deserializer(serialized_value, is_required):
    parts = serialized_value.split("-")
    start_coordinates = parts[0].split(":")
    start = Point(int(start_coordinates[0][1:]), int(start_coordinates[1]))
    end_coordinates = parts[1].split(":")
    end = Point(int(end_coordinates[0][1:]), int(end_coordinates[1]))
    return Position(start, end)