import unittest

from pylasu.model import Point
from pylasu.parsing.parse_tree import ParseTreeOrigin
from tests.simple_lang.SimpleLangLexer import SimpleLangLexer
from tests.simple_lang.SimpleLangParser import SimpleLangParser
from antlr4 import CommonTokenStream, InputStream


class ParseTreeTest(unittest.TestCase):
    def test_parse_tree_origin(self):
        lexer = SimpleLangLexer(InputStream("display\n42"))
        parser = SimpleLangParser(CommonTokenStream(lexer))
        parse_tree = parser.compilationUnit()
        origin = ParseTreeOrigin(parse_tree)
        position = origin.position
        self.assertIsNotNone(position)
        self.assertEqual(position.start, Point(1, 0))
        self.assertEqual(position.end, Point(2, 2))
