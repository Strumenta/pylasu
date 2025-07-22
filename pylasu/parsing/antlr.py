import time
from abc import abstractmethod
from typing import Optional, List

from antlr4 import CommonTokenStream, InputStream, Lexer, Parser, ParserATNSimulator, ParserRuleContext, \
    PredictionContextCache, Recognizer, Token, TokenStream
from antlr4.error.ErrorListener import ErrorListener
from pylasu.model import walk, Source, Position, Node, Point
from pylasu.model.processing import assign_parents
from pylasu.parsing.parse_tree import token_end_point
from pylasu.parsing.results import ParsingResultWithFirstStage, FirstStageParsingResult
from pylasu.validation import Issue, IssueType


class PylasuANTLRParser:
    """ A complete description of a multi-stage ANTLR-based parser, from source code to AST.

    You should extend this class to implement the parts that are specific to your language.

    Note: instances of this class are thread-safe and they're meant to be reused. Do not create a new PylasuANTLRParser
    instance every time you need to parse some source code, or performance may suffer."""
    def __init__(self):
        self.prediction_context_cache = PredictionContextCache()

    def parse(self, input_stream: InputStream, consider_range: bool = True, measure_lexing_time: bool = False,
              source: Optional[Source] = None):
        """Parses source code, returning a result that includes an AST and a collection of parse issues
        (errors, warnings).
        The parsing is done in accordance to the StarLasu methodology i.e. a first-stage parser builds a parse tree
        which is then mapped onto a higher-level tree called the AST.
        @param inputStream the source code.
        @param charset the character set in which the input is encoded.
        @param considerPosition if true (the default), parsed AST nodes record their position in the input text.
        @param measureLexingTime if true, the result will include a measurement of the time spent in lexing i.e.
        breaking the input stream into tokens."""
        start = time.time_ns()
        first_stage = self.parse_first_stage(input_stream, measure_lexing_time)
        issues = first_stage.issues
        ast = self.parse_tree_to_ast(first_stage.root, consider_range, issues, source)
        self.assign_parents(ast)
        ast = self.post_process_ast(ast, issues) if ast else ast
        if ast and not consider_range:
            # Remove parseTreeNodes because they cause the range to be computed
            for node in walk(ast):
                node.origin = None
        now = time.time_ns()
        return ParsingResultWithFirstStage(
            issues,
            ast,
            input_stream.getText(0, input_stream.index + 1),
            (now - start) // 1_000_000,
            first_stage,
            source,
        )

    def parse_first_stage(
            self, input_stream: InputStream, measure_lexing_time: bool = False, source: Source = None
    ) -> FirstStageParsingResult:
        """Executes only the first stage of the parser, i.e., the production of a parse tree. Usually, you'll want to
        use the [parse] method, that returns an AST which is simpler to use and query."""
        issues = []
        lexing_time: Optional[int] = None
        total_time: int = time.time_ns()
        parser = self.create_parser(input_stream, issues)
        if measure_lexing_time:
            token_stream = parser.getInputStream()
            if isinstance(token_stream, CommonTokenStream):
                lexing_time = time.time_ns()
                token_stream.fill()
                token_stream.seek(0)
                lexing_time = (time.time_ns() - lexing_time) // 1_000_000
        root = self.invoke_root_rule(parser)
        if root:
            self.verify_parse_tree(parser, issues, root)
        total_time = (time.time_ns() - total_time) // 1_000_000
        return FirstStageParsingResult(issues, root, None, total_time, lexing_time, source)

    def create_parser(self, input_stream: InputStream, issues: List[Issue]) -> Parser:
        """Creates the first-stage parser."""
        lexer = self.create_antlr_lexer(input_stream)
        self.attach_listeners(lexer, issues)
        token_stream = self.create_token_stream(lexer)
        parser = self.create_antlr_parser(token_stream)
        # Assign interpreter to avoid caching DFA states indefinitely across executions
        parser._interp = \
            ParserATNSimulator(parser, parser.atn, parser._interp.decisionToDFA, self.prediction_context_cache)
        self.attach_listeners(parser, issues)
        return parser

    def invoke_root_rule(self, parser: Parser):
        """Invokes the parser's root rule, i.e., the method which is responsible for parsing the entire input.
        Usually this is the topmost rule, the one with index 0 (as also assumed by other libraries such as antlr4-c3),
        so this method invokes that rule. If your grammar/parser is structured differently, or if you're using this to
        parse only a portion of the input or a subset of the language, you have to override this method to invoke the
        correct entry point."""
        return getattr(parser, parser.ruleNames[0])()

    def verify_parse_tree(self, parser: Parser, issues: List[Issue], root: ParserRuleContext):
        """Checks the parse tree for correctness.
        If you're concerned about performance, you may want to override this to do nothing."""
        last_token: Token = parser.getTokenStream().get(parser.getTokenStream().index)
        if last_token.type != Token.EOF:
            issues.append(
                Issue(
                    IssueType.SYNTACTIC,
                    "The whole input was not consumed",
                    position=Position(token_end_point(last_token), token_end_point(last_token))
                )
            )
        # TODO Kolasu also traverses the parse tree searching for exceptions

    def assign_parents(self, ast):
        if ast:
            assign_parents(ast)

    def post_process_ast(self, ast, issues):
        return ast

    def create_token_stream(self, lexer: Lexer) -> TokenStream:
        return CommonTokenStream(lexer)

    @abstractmethod
    def create_antlr_lexer(self, input_stream: InputStream):
        """Creates the lexer."""
        pass

    @abstractmethod
    def create_antlr_parser(self, token_stream: TokenStream):
        """Creates the first-stage parser."""
        pass

    @abstractmethod
    def parse_tree_to_ast(self, root, consider_range: bool, issues: List[Issue], source: Source) -> Optional[Node]:
        pass

    def attach_listeners(self, recognizer: Recognizer, issues: List[Issue]):
        recognizer.removeErrorListeners()
        recognizer.addErrorListener(ParserErrorListener(issues))


class ParserErrorListener(ErrorListener):
    def __init__(self, issues: List[Issue]):
        self.issues = issues

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        start_point = Point(line, column)
        end_point = start_point
        if isinstance(offending_symbol, Token):
            end_point = token_end_point(offending_symbol)
        self.issues.append(Issue(IssueType.SYNTACTIC, msg or "unspecified", position=Position(start_point, end_point)))
