from typing import Optional

from lionwebpython.language import Concept
from lionwebpython.model.impl.dynamic_node import DynamicNode

from pylasu.model import Position


class ASTNode(DynamicNode):

    def __init__(self, id: str, concept: Concept, position: Optional[Position] = None):
        super().__init__(id=id, concept=concept)
        if position:
            self.set_property_value(property=concept.get_property_by_name('position'), value=position)
