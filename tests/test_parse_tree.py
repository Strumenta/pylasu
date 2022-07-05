import os
import unittest

from antlr4 import CommonTokenStream, InputStream

from pylasu.model import Point
from pylasu.parsing.parse_tree import ParseTreeOrigin, generate_nodes_classes_for_parser
from tests.simple_lang.SimpleLangLexer import SimpleLangLexer
from tests.simple_lang.SimpleLangParser import SimpleLangParser


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

    def test_ast_gen(self):
        generate_nodes_classes_for_parser(SimpleLangParser, globals())
        self.assertTrue("CompilationUnit" in globals())
        CompilationUnit = globals()["CompilationUnit"]
        cu = CompilationUnit(syntax_before="# Generated" + os.linesep, syntax_after=os.linesep + "# End")
        self.assertIsNotNone(cu)
        self.assertTrue(("statement_list", []) in cu.properties)
        self.assertEqual("""# Generated

# End""", cu.to_string())

    def test_parsing_unparsing_roundtrip(self):
        code = "display\n42"
        lexer = SimpleLangLexer(InputStream(code))
        parser = SimpleLangParser(CommonTokenStream(lexer))
        parse_tree = parser.compilationUnit()
        generate_nodes_classes_for_parser(SimpleLangParser, globals())
        CompilationUnit = globals()["CompilationUnit"]
        cu = CompilationUnit.from_parse_tree(parse_tree)
        self.assertEqual(code, cu.to_string())
