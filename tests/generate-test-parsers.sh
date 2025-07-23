antlr4 -Dlanguage=Python3 -visitor -o simple_lang SimpleLangLexer.g4 SimpleLangParser.g4
antlr4 -Dlanguage=Python3 -visitor -o antlr_entity AntlrEntityLexer.g4 AntlrEntityParser.g4
antlr4 -Dlanguage=Python3 -visitor -o antlr_script AntlrScriptLexer.g4 AntlrScriptParser.g4
