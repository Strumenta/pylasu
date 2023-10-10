java -cp ../antlr-4.11.1-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 -visitor -o simple_lang SimpleLangLexer.g4 SimpleLangParser.g4
java -cp ../antlr-4.11.1-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 -visitor -o antlr_entity AntlrEntityLexer.g4 AntlrEntityParser.g4
java -cp ../antlr-4.11.1-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 -visitor -o antlr_script AntlrScriptLexer.g4 AntlrScriptParser.g4
