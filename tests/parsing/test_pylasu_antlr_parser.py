import unittest
from typing import List, Optional

from antlr4 import TokenStream, InputStream

from pylasu.model import Source, Node, Position, Point
from pylasu.parsing.antlr import PylasuANTLRParser
from pylasu.validation import Issue
from tests.simple_lang.SimpleLangLexer import SimpleLangLexer
from tests.simple_lang.SimpleLangParser import SimpleLangParser


class SimpleLangPylasuParser(PylasuANTLRParser):

    def create_antlr_lexer(self, input_stream: InputStream):
        return SimpleLangLexer(input_stream)

    def create_antlr_parser(self, token_stream: TokenStream):
        return SimpleLangParser(token_stream)

    def parse_tree_to_ast(self, root, consider_range: bool, issues: List[Issue], source: Source) -> Optional[Node]:
        return None


class KolasuParserTest(unittest.TestCase):
    def test_lexing(self):
        parser = SimpleLangPylasuParser()
        result = parser.parse("""set a = 10
set b = ""
display c
""")
        self.assertIsNotNone(result)
        # TODO we don't have Pylasu Tokens yet

    def test_issues_are_capitalized(self):
        parser = SimpleLangPylasuParser()
        result = parser.parse("""set set a = 10
display c
""")
        self.assertTrue(result.issues)
        self.assertTrue([i for i in result.issues if i.message.startswith("Extraneous input 'set'")])
        self.assertTrue([i for i in result.issues if i.message.startswith("Mismatched input 'c'")])

    def test_issues_have_not_flat_position(self):
        parser = SimpleLangPylasuParser()
        result = parser.parse("""set set a = 10
display c
""")
        self.assertTrue(result.issues)
        extraneous_input = [i for i in result.issues if i.message.startswith("Extraneous input 'set'")][0]
        self.assertEqual(Position(Point(1, 4), Point(1, 7)), extraneous_input.position)
        mismatched_input = [i for i in result.issues if i.message.startswith("Mismatched input 'c'")][0]
        self.assertEqual(Position(Point(2, 8), Point(2, 9)), mismatched_input.position)
