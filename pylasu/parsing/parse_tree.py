from dataclasses import dataclass, field
from typing import Optional, List, Sequence

from antlr4 import ParserRuleContext, TerminalNode, Token
from antlr4.tree.Tree import ParseTree

from pylasu.model import Origin, Position, Point
from pylasu.model.model import internal_property, Node
from pylasu.model.position import Source
from pylasu.support import extension_method
from pylasu.transformation.printing import NodeWithSyntax

import inspect


@dataclass
class ParseTreeOrigin(Origin):
    parse_tree: ParseTree
    source: Source = None

    @internal_property
    def position(self) -> Optional[Position]:
        return self.parse_tree.to_position(self.source)

    @internal_property
    def source_text(self) -> Optional[str]:
        if isinstance(self.parse_tree, ParserRuleContext):
            return self.parse_tree.get_original_text()
        elif isinstance(self.parse_tree, TerminalNode):
            return self.parse_tree.getText()
        else:
            return None


def token_start_point(token: Token):
    return Point(token.line, token.column)


def token_end_point(token: Token):
    if token.type == Token.EOF:
        return token.start_point
    else:
        return token.start_point + token.text


Token.start_point = property(token_start_point)
Token.end_point = property(token_end_point)


@extension_method(ParserRuleContext)
def to_position(self: ParserRuleContext, source: Source = None):
    if self.start.start_point <= self.stop.end_point:
        return Position(self.start.start_point, self.stop.end_point, source)
    else:
        # In case of parse errors, sometimes ANTLR inserts nodes that end before they start
        return Position(self.start.start_point, self.start.end_point, source)


@extension_method(TerminalNode)
def to_position(self: TerminalNode, source: Source = None):
    return self.symbol.to_position(source)


@extension_method(Token)
def to_position(self: Token, source: Source = None):
    return Position(self.start_point, self.end_point, source)


@extension_method(ParserRuleContext)
def get_original_text(self: ParserRuleContext) -> str:
    a = self.start.start
    b = self.stop.stop
    return self.start.getInputStream().getText(a, b)


@extension_method(Node)
def with_parse_tree(self: Node, tree: ParseTree, source: Source = None):
    self.origin = ParseTreeOrigin(parse_tree=tree, source=source)
    return self


def generate_nodes_classes_for_parser(parser_class: type, ns: dict):
    for name, definition in parse_tree_node_definitions(parser_class):
        fields = {"__annotations__": {}}
        property_names = []
        aliases = {}
        for child_name, value in parse_tree_node_children(definition):
            default_value = None
            field_type = None
            if inspect.isfunction(value):
                n_args = len(inspect.signature(value).parameters)
                if n_args == 2:
                    suffix = "_list"
                    child_name += suffix
                    field_type = List
                    default_value = field(default_factory=list)
                    aliases[child_name] = child_name[:-len(suffix)]
            fields[child_name] = default_value
            fields["__annotations__"][child_name] = field_type
            property_names.append(child_name)
        name = ast_node_name(name)
        class_def = type(name, (NodeWithSyntax,), fields)
        class_def.properties = properties_method(property_names)
        class_def.from_parse_tree = from_parse_tree_function(class_def, property_names, aliases, ns)
        ns[name] = dataclass(class_def)


def ast_node_name(parse_tree_node_name):
    if parse_tree_node_name.endswith("Context"):
        parse_tree_node_name = parse_tree_node_name[:-len("Context")]
    return parse_tree_node_name


def properties_method(property_names):
    return internal_property(lambda node: ((p, getattr(node, p)) for p in property_names))


def stop_token(node):
    if isinstance(node, TerminalNode):
        return node.symbol
    elif isinstance(node, ParserRuleContext):
        return node.stop


def start_token(node):
    if isinstance(node, TerminalNode):
        return node.symbol
    elif isinstance(node, ParserRuleContext):
        return node.start


def make_ast_node_or_value(parse_tree_node, prev_node, ns, parent: Node, source: Source):
    ast_node_type_name = ast_node_name(type(parse_tree_node).__name__)
    if ast_node_type_name in ns:
        ast_node = ns[ast_node_type_name].from_parse_tree(parse_tree_node, parent, source)
        if isinstance(parent.origin, ParseTreeOrigin):
            if prev_node is not None and prev_node.to_position() is not None:
                a = stop_token(prev_node).stop
                b = start_token(parse_tree_node).start
                if a < b:
                    ast_node.syntax_before = parent.origin.parse_tree.start.getInputStream().getText(a + 1, b)
        return ast_node
    else:
        return parse_tree_node.getText()


def from_parse_tree_function(node_class, property_names, aliases, ns: dict):
    def from_parse_tree(parse_tree: ParseTree, parent: Node = None, source: Source = None):
        node = node_class().with_parent(parent).with_parse_tree(parse_tree, source)
        last_pt_node = parse_tree
        for prop in property_names:
            if prop in aliases:
                pt_prop = aliases[prop]
            else:
                pt_prop = prop
            prop_val = getattr(parse_tree, pt_prop)
            if inspect.ismethod(prop_val):
                prop_val = prop_val()
            if isinstance(prop_val, Sequence) and not isinstance(prop_val, str):
                children = []
                for child in prop_val:
                    children.append(make_ast_node_or_value(child, last_pt_node, ns, node, source))
                    last_pt_node = child
                setattr(node, prop, children)
            elif prop_val is not None:
                setattr(node, prop, make_ast_node_or_value(prop_val, last_pt_node, ns, node, source))
                last_pt_node = prop_val
        return node
    return from_parse_tree


def parse_tree_node_definitions(parser_class: type):
    for name in dir(parser_class):
        definition = getattr(parser_class, name)
        if isinstance(definition, type) and name != "__class__":
            yield name, definition


def parse_tree_node_children(parse_tree_node_class: type):
    for x in dir(parse_tree_node_class):
        if x not in dir(ParserRuleContext) and x != "parser":
            yield x, getattr(parse_tree_node_class, x)
