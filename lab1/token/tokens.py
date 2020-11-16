from functools import partial
from .automaton_matching import integer_match, double_match, identifier_match

def match(*args):
    """check if input matches any possible matches, checks as many chars as the input text"""

    text = args[-1]
    text_l = len(text)
    for matching in args[:-1]:
        if matching[:text_l] == text:
            if text_l == len(matching):
                return True     #full match

            return None         #not closed

    return False                #not matched

def comment_match(input):
    """comment matcher"""

    if input[:2] == "/*"[:len(input)]:
        if input[-2:] == "*/":
            return True         #full match

        return None             #not closed

    #C-type or Unix-type single line comment
    if input[:2] == "//"[:len(input)] or input[0] == "#":
        if input[-1:] == "\n":
            return True         #full match

        return None             #not closed

    return False                #not matched

def doc_match(input):
    """doc-string matcher"""
    if input[:3] == "/**"[:len(input)]:
        if input[-2:] == "*/":
            return True         #full match

        return None             #not closed

    return False                #not matched

def string_match(input):
    """usual string matcher"""

    #string input using ""
    if input[0] == "\"":
        if len(input) > 1 and input[-1:] == "\"" and input[-2:] != "\\\"":
            return True         #full match

        return None             #not closed

    
    #string input using ''
    if input[0] == "\'":
        if len(input) > 1 and input[-1:] == "\'" and input[-2:] != "\\\'":
            return True         #full match

        return None             #not closed

    return False                #not matched


tokens = {
    "T_ABSTRACT": partial(match, "abstract"),
    "T_AND_EQUAL": partial(match, "&="),
    "T_ARRAY": partial(match, "array"),
    "T_ARRAY_CAST": partial(match, "(array)"),
    "T_AS": partial(match, "as"),
    "T_BOOLEAN_AND": partial(match, "&&"),
    "T_BOOLEAN_OR": partial(match, "||"),
    "T_BOOL_CAST": partial(match, "(bool)", "(boolean)"),
    "T_BREAK": partial(match, "break"),
    "T_CALLABLE": partial(match, "callable"),
    "T_CASE": partial(match, "case"),
    "T_CATCH": partial(match, "catch"),
    "T_CLASS": partial(match, "class"),
    "T_CLASS_C": partial(match, "__CLASS__"),
    "T_CLONE": partial(match, "clone"),
    "T_CLOSE_TAG": partial(match, "?>", "%>"),
    "T_COALESCE": partial(match, "??"),
    "T_COALESCE_EQUAL": partial(match, "??="),
    "T_COMMENT": comment_match,
    "T_CONCAT_EQUAL": partial(match, ".="),
    "T_CONST": partial(match, "const"),
    "T_CONSTANT_ENCAPSED_STRING": string_match,
    "T_CONTINUE": partial(match, "continue"),
    "T_DEC": partial(match, "--"),
    "T_DECLARE": partial(match, "declare"),
    "T_DEFAULT": partial(match, "default"),
    "T_DIR": partial(match, "__DIR__"),
    "T_DIV_EQUAL": partial(match, "/="),
    "T_DNUMBER": double_match,
    "T_DO": partial(match, "do"),
    "T_DOC_COMMENT": doc_match,
    "T_DOUBLE_ARROW": partial(match, "=>"),
    "T_DOUBLE_CAST": partial(match, "(real)", "(double)", "(float)"),
    "T_DOUBLE_COLON": partial(match, "::"),
    "T_ECHO": partial(match, "echo"),
    "T_ELLIPSIS": partial(match, "..."),
    "T_ELSE": partial(match, "else"),
    "T_ELSEIF": partial(match, "elseif"),
    "T_EMPTY": partial(match, "empty"),
    "T_ENDDECLARE": partial(match, "enddeclare"),
    "T_ENDFOR": partial(match, "endfor"),
    "T_ENDFOREACH": partial(match, "endforeach"),
    "T_ENDIF": partial(match, "endif"),
    "T_ENDSWITCH": partial(match, "endswitch"),
    "T_ENDWHILE": partial(match, "endwhile"),
    "T_EVAL": partial(match, "eval"),
    "T_EXIT": partial(match, "exit", "die"),
    "T_EXTENDS": partial(match, "extends"),
    "T_FILE": partial(match, "__FILE__"),
    "T_FINAL": partial(match, "final"),
    "T_FINALLY": partial(match, "finally"),
    "T_FN": partial(match, "fn"),
    "T_FOR": partial(match, "for"),
    "T_FOREACH": partial(match, "foreach"),
    "T_FUNCTION": partial(match, "function"),
    "T_FUNC_C": partial(match, "__FUNCTION__"),
    "T_GLOBAL": partial(match, "global"),
    "T_GOTO": partial(match, "goto"),
    "T_HALT_COMPILER": partial(match, "__halt_compiler"),
    "T_IF": partial(match, "if"),
    "T_IMPLEMENTS": partial(match, "implements"),
    "T_INC": partial(match, "++"),
    "T_INCULDE": partial(match, "include"),
    "T_INCLUDE_ONCE": partial(match, "include_once"),
    "T_INSTANCEOF": partial(match, "instanceof"),
    "T_INSTEADOF": partial(match, "insteadof"),
    "T_INTERFACE": partial(match, "interface"),
    "T_INT_CAST": partial(match, "(int)", "(integer)"),
    "T_ISSET": partial(match, "isset"),
    "T_IS_EQUAL": partial(match, "=="),
    "T_IS_GREATER_OR_EQUAL": partial(match, ">="),
    "T_IS_IDENTICAL": partial(match, "==="),
    "T_IS_NOT_EQUAL": partial(match, "!=", "<>"),
    "T_IS_NOT_IDENTICAL": partial(match, "!=="),
    "T_IS_SMALLER_OR_EQUAL": partial(match, "<="),
    "T_LINE": partial(match, "__LINE__"),
    "T_LIST": partial(match, "list"),
    "T_LNUMBER": integer_match,
    "T_LOGICAL_AND": partial(match, "and"),
    "T_LOGICAL_OR": partial(match, "or"),
    "T_LOGICAR_XOR": partial(match, "xor"),
    "T_METHOD_C": partial(match, "__METHOD__"),
    "T_MINUS_EQUAL": partial(match, "-="),
    "T_MOD_EQUAL": partial(match, "%="),
    "T_MUL_EQUAL": partial(match, "*="),
    "T_NAMESPACE": partial(match, "namespace"),
    "T_NEW": partial(match, "new"),
    "T_NS_C": partial(match, "__NAMESPACE__"),
    "T_NS_SEPARATOR": partial(match, "\\"),
    "T_OBJECT_CAST": partial(match, "(object)"),
    "T_OBJECT_OPERATOR": partial(match, "->"),
    "T_OPEN_TAG": partial(match, "<?php", "<?", "<%"),
    "T_OPEN_TAG_WITH_ECHO": partial(match, "<?=", "<%="),
    "T_OR_EQUAL": partial(match, "|="),
    "T_DOUBLE_COLON": partial(match, "::"),
    "T_PLUS_EQUAL": partial(match, "+="),
    "T_POW": partial(match, "**"),
    "T_POW_EQUAL": partial(match, "**="),
    "T_PRINT": partial(match, "print"),
    "T_PRIVATE": partial(match, "private"),
    "T_PROTECTED": partial(match, "protected"),
    "T_PUBLIC": partial(match, "public"),
    "T_REQUIRE": partial(match, "require"),
    "T_REQUIRE_ONCE": partial(match, "require_once"),
    "T_RETURN": partial(match, "return"),
    "T_SL": partial(match, "<<"),
    "T_SL_EQUAL": partial(match, "<<="),
    "T_SPACESHIP": partial(match, "<=>"),
    "T_SR": partial(match, ">>"),
    "T_SR_EQUAL": partial(match, ">>="),
    "T_START_HEREDOC": partial(match, "<<<"),
    "T_STATIC": partial(match, "static"),
    "T_STRING": identifier_match,
    "T_STRING_CAST": partial(match, "(string)"),
    "T_SWITCH": partial(match, "switch"),
    "T_THROW": partial(match, "throw"),
    "T_TRAIT": partial(match, "trait"),
    "T_TRAIT_C": partial(match, "__TRAIT__"),
    "T_TRY": partial(match, "try"),
    "T_UNSET": partial(match, "unset"),
    "T_UNSET_CAST": partial(match, "(unset)"),
    "T_USE": partial(match, "use"),
    "T_VAR": partial(match, "var"),
    "T_VARIABLE": lambda input: match("$", input[:1]) and identifier_match(input[1:]),
    "T_WHILE": partial(match, "while"),
    "T_XOR_EQUAL": partial(match, "^="),
    "T_YIELD": partial(match, "yield"),
    "T_YIELD_FROM": partial(match, "yield from"),
    "R_PARENTHESES_OPEN": partial(match, "("),
    "R_PARENTHESES_CLOSE": partial(match, ")"),
    "S_PARENTHESES_OPEN": partial(match, "["),
    "S_PARENTHESES_CLOSE": partial(match, "]"),
    "BRACKET_OPEN": partial(match, "{"),
    "BRACKET_CLOSE": partial(match, "}"),
    "SEMICOLON": partial(match, ";"),
    "COMMA": partial(match, ","),
    "DOT": partial(match, "."),
    "EQUAL": partial(match, "="),
    "Q_MARK": partial(match, "?"),
    "COLON": partial(match, ":"),
    "LESS_THAN": partial(match, "<"),
    "MORE_THAN": partial(match, ">"),
    "MINUS": partial(match, "-"),
    "PLUS": partial(match, "+"),
    "BITWISE_OR": partial(match, "|"),
    "BITWISE_AND": partial(match, "&"),
    "BITWISE_XOR": partial(match, "^"),
    "MULTIPLY": partial(match, "*"),
    "DIVIDE": partial(match, "/"),
    "MODULO": partial(match, "%"),
    "RX_MARK": partial(match, "!"),
}

def detect_token(to_check):
    """
    function that uses existing tokens dictionary
    and tries to match input string using matcher
    functions, that are provided as values in
    tokens dictionary

    to_check: string that is being tokenized
    """

    gave_true = []
    gave_none = []

    for token, matcher in tokens.items():
        res = matcher(to_check)

        if res != False:
            if res == True:
                gave_true.append(token)

            elif res == None:
                gave_none.append(token)

    questionable = ["T_STRING", "T_VARIABLE", "T_LNUMBER", "T_DNUMBER"]

    for possible_token in gave_true:
        if possible_token in questionable:
            gave_none.append(possible_token)    #questionable tokens have variable length, putting in none so that they're read in full

    if len(gave_true) == 2 and "T_STRING" in gave_true:
        gave_true.remove("T_STRING")        #special case - T_STRING is any identifier, will collide with any keyword

    if len(gave_true) == 2 and "T_DOC_COMMENT" in gave_true:    #another collision
        gave_true.remove("T_COMMENT")

    return {"true": gave_true, "none": gave_none}