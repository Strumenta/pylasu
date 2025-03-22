from typing import Optional

from lionwebpython.model.classifier_instance_utils import ClassifierInstanceUtils
from lionwebpython.model.impl.dynamic_node import DynamicNode
from lionwebpython.model.node import Node


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

    def __init__(self, language_name: str, relative_path: str, code: str, ast: Optional[Node] = None,
                 id: Optional[str] = None):
        from pylasu.lionweb.utils import to_lionweb_identifier
        from pylasu.codebase.lwlanguage import CODEBASE_FILE
        super().__init__(id or f"codebase_file_{to_lionweb_identifier(relative_path)}", CODEBASE_FILE)
        self.language_name = language_name
        self.relative_path = relative_path
        self.code = code
        self.ast = ast
