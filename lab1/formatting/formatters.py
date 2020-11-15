from util.util import *
from functools import partial

#Indents formatters
def apply_indent(tokens, curr_token_index, config):
    """Applies indent specified in config"""
    res = {"before": "", "after": ""}

    indent = int(config["Indents"]["Indent"])

    if indent != 0 and check_if_first_token_in_line(tokens, curr_token_index):
        nesting_level = count_token_nesting(tokens, curr_token_index, ["BRACKET_OPEN"], ["BRACKET_CLOSE"])

        res["before"] += " " * indent * nesting_level
    
    return res

def apply_continue_indent(tokens, curr_token_index, config):
    """Applies continuation indent specified in config"""

    res = {"before": "", "after": ""}

    cont_indent = int(config["Indents"]["Continuation indent"])

    if (cont_indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
        and not previous_token_is_semicolon(tokens, curr_token_index)):

        res["before"] += " " * cont_indent

    return res

def apply_indent_in_php_tags(tokens, curr_token_index, config):
    """Applies indent specified in configs
    if php tags indent flag is set to True"""
    res = {"before": "", "after": ""}

    indent = int(config["Indents"]["Indent"])

    if (indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
        and config["Indents"]["Indent code in PHP tags"] == "True"):

        nesting_level = count_token_nesting(tokens, curr_token_index, ["T_OPEN_TAG", "T_OPEN_TAG_WITH_ECHO"], ["T_CLOSE_TAG"])

        res["before"] += " " * indent * nesting_level

    return res

#Spaces before parentheses formatters
def func_decl_parentheses(tokens, curr_token_index, config):
    """Puts space between function declaration
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["Function declaration parentheses"] == "True"
        and check_if_func_declared(tokens, curr_token_index)):

        res["after"] += " "

    return res

def func_call_paretheses(tokens, curr_token_index, config):
    """Puts space between function call
    and paretheses if flag set to True"""
    res = {"before": "", "after": ""}

    if (config["Spaces"]["Function call parentheses"] == "True"
        and check_if_func_call(tokens, curr_token_index)):

        res["after"] += " "

    return res

def _token_and_parentheses(config_key, interest_token, tokens, curr_token_index, config):
    """Puts space between token of interest 
    and paretheses if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"][config_key] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, interest_token)):

        res["after"] += " "

    return res

anon_func_paretheses = partial(_token_and_parentheses, "Anonymous function parentheses", "T_FUNCTION")
if_parentheses = partial(_token_and_parentheses, "'if' parentheses", "T_IF")
for_parentheses = partial(_token_and_parentheses, "'for' parentheses", "T_FOR")
while_parentheses = partial(_token_and_parentheses, "'while' parentheses", "T_WHILE")
switch_parentheses = partial(_token_and_parentheses, "'switch' parentheses", "T_SWITCH")
catch_parentheses = partial(_token_and_parentheses, "'catch' parentheses", "T_CATCH")
array_init_parentheses = partial(_token_and_parentheses, "Array initializer parentheses", "T_ARRAY")

#Spaces around operators
def _around_token(config_key, interest_tokens, tokens, curr_token_index, config):
    """Puts spaces around token of interest 
    if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"][config_key] == "True" and tokens[curr_token_index] in interest_tokens:
        res["after"] += " "
        res["before"] += " "

    return res

assign_operators = partial(_around_token, "Assignment operators (=, +=, ...)",
                           [
                               "EQUAL", "T_AND_EQUAL", "T_DOUBLE_ARROW", "T_COALESCE_EQUAL", "T_CONCAT_EQUAL",
                               "T_DIV_EQUAL", "T_DOUBLE_ARROW", "T_OR_EQUAL", "T_PLUS_EQUAL", "T_POW_EQUAL",
                               "T_SL_EQUAL", "T_SR_EQUAL", "T_XOR_EQUAL"
                           ]
                          )
logical_operators = partial(_around_token, "Logical operators (&&, ||)", ["T_BOOLEAN_AND", "T_BOOLEAN_OR"])
equality_operators = partial(_around_token, "Equality operators (==, !=)", ["T_IS_EQUAL", "T_IS_IDENTICAL", "T_IS_NOT_EQUAL", "T_IS_NOT_IDENTICAL"])
relational_operators = partial(_around_token, "Relational operators (<, >, <=, >=, <=>)",
                                ["LESS_THAN", "MORE_THAN", "T_IS_GREATER_OR_EQUAL", "T_IS_SMALLER_OR_EQUAL", "T_SPACESHIP"]
                              )
bitwise_operators = partial(_around_token, "Bitwise operators (&, |, ^)", ["BITWISE_OR", "BITWISE_AND", "BITWISE_XOR"])
additive_operators = partial(_around_token, "Additive operators (+, -)", ["PLUS", "MINUS"])
multiplicative_operators = partial(_around_token, "Multiplicative operators (*, /, %, **)", ["MULTIPLY", "MODULO", "DIVIDE", "T_POW"])
shift_operators = partial(_around_token, "Shift operators (<<, >>)", ["T_SL", "T_SR"])
unary_operators = partial(_around_token, "Unary additive operators (+, -, ++, --)", ["UNARY_PLUS", "UNARY_MINUS", "T_DEC", "T_INC"])
concat_operator = partial(_around_token, "Concatenation (.)", ["DOT"])
obj_access_operator = partial(_around_token, "Object access operator (->)", ["T_OBJECT_OPERATOR"])
null_coal_operator = partial(_around_token, "Null coalescing operator (??)", ["T_COALESCE"])
null_coal_operator = partial(_around_token, "Null coalescing operator (??)", ["T_COALESCE"])

def assignment_in_declare(tokens, curr_token_index, config):
    """Puts spaces around assignment in declare construct 
    if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["Assignment in declare statement"] == "True" 
        and check_assign_in_declare(tokens, curr_token_index)):
        res["after"] += " "
        res["before"] += " "

    return res

#Space before left brace
def class_declaration_left_brace(tokens, curr_token_index, config):
    """Puts space before left brace in class declaration
    if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["Class left brace"] == "True" 
        and check_class_declaration(tokens, curr_token_index)):
        res["before"] += " "

    return res

def func_declaration_left_brace(tokens, curr_token_index, config):
    """Puts space before left brace in function declaration
    if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["Function left brace"] == "True" 
        and check_function_declaration_left_brace(tokens, curr_token_index)):
        res["before"] += " "

    return res

def _left_brace_after_token(config_key, interest_token, tokens, curr_token_index, config):
    """Puts space before left brace
    that follows interest_token and
    if flag in config_key is set to True;
    this function skips some other tokens in between"""

    res = {"before": "", "after": ""}

    if (config["Spaces"][config_key] == "True" 
        and check_left_brace_after_token(tokens, curr_token_index, interest_token)):

        res["before"] += " "

    return res

if_left_brace = partial(_left_brace_after_token, "'if' left brace", "T_IF")
else_left_brace = partial(_left_brace_after_token, "'else' left brace", "T_ELSE")
elseif_left_brace = partial(_left_brace_after_token, "'else' left brace", "T_ELSEIF")     #share one rule
for_left_brace = partial(_left_brace_after_token, "'for' left brace", "T_FOR")
while_left_brace = partial(_left_brace_after_token, "'while' left brace", "T_WHILE")
do_left_brace = partial(_left_brace_after_token, "'do' left brace", "T_DO")
switch_left_brace = partial(_left_brace_after_token, "'switch' left brace", "T_SWITCH")
try_left_brace = partial(_left_brace_after_token, "'try' left brace", "T_TRY")
catch_left_brace = partial(_left_brace_after_token, "'catch' left brace", "T_CATCH")
finally_left_brace = partial(_left_brace_after_token, "'finally' left brace", "T_FINALLY")

#Spaces before keywords
def _before_token(config_key, interest_token, tokens, curr_token_index, config):
    """Puts space before specified token
    if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"][config_key] == "True" and tokens[curr_token_index] == interest_token):
        res["before"] += " "

    return res


before_else = partial(_before_token, "'else' keyword", "T_ELSE")
before_while = partial(_before_token, "'while' keyword", "T_WHILE")
before_catch = partial(_before_token, "'catch' keyword", "T_CATCH")
before_finally = partial(_before_token, "'finally' keyword", "T_FINALLY")

#Spaces within
def in_brackets(tokens, curr_token_index, config):
    """Puts spaces within brackets
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["Brackets"] == "True":
        if tokens[curr_token_index] == "S_PARENTHESES_OPEN":
            res["after"] += " "

        if tokens[curr_token_index] == "S_PARENTHESES_CLOSE":
            res["before"] += " "

    return res

def in_func_decl_parentheses(tokens, curr_token_index, config):
    """Puts spaces within function declaration parantheses
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["Within function declaration parentheses"] == "True":
        if check_left_brace_after_func_decl(tokens, curr_token_index):
            res["after"] += " "

        if check_right_brace_after_func_decl(tokens, curr_token_index):
            res["before"] += " "

    return res

def _in_token_parentheses(config_key, interest_token, tokens, curr_token_index, config):
    """Puts spaces within arguments
    parantheses of specified token
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"][config_key] == "True":
        if check_if_left_parentheses_after_token(tokens, curr_token_index, interest_token):
            res["after"] += " "

        if check_if_right_parentheses_after_token(tokens, curr_token_index, interest_token):
            res["before"] += " "

    return res

in_array_init_parentheses = partial(_in_token_parentheses, "Within array initializer parentheses", "T_ARRAY")
in_func_call_parentheses = partial(_in_token_parentheses, "Within array initializer parentheses", "T_STRING")
in_if_parentheses = partial(_in_token_parentheses, "Within 'if' parentheses", "T_IF")
in_for_parentheses = partial(_in_token_parentheses, "Within 'for' parentheses", "T_FOR")
in_while_parentheses = partial(_in_token_parentheses, "Within 'while' parentheses", "T_WHILE")
in_switch_parentheses = partial(_in_token_parentheses, "Within 'switch' parentheses", "T_SWITCH")
in_catch_parentheses = partial(_in_token_parentheses, "Within 'catch' parentheses", "T_CATCH")

def in_grouping_parentheses(tokens, curr_token_index, config):
    """Puts spaces within parantheses that aren't any of the above
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["Grouping parentheses"] == "True":
        if tokens[curr_token_index] == "R_PARENTHESES_OPEN":
            if not check_left_brace_after_func_decl(tokens, curr_token_index):
                for token in ["T_ARRAY","T_STRING","T_IF","T_WHILE","T_SWITCH","T_CATCH","T_FOR"]:
                    if check_if_left_parentheses_after_token(tokens, curr_token_index, token):
                        break

                    else:
                        res["after"] += " "

        if tokens[curr_token_index] == "R_PARENTHESES_CLOSE":
            if not check_right_brace_after_func_decl(tokens, curr_token_index):
                for token in ["T_ARRAY","T_STRING","T_IF","T_WHILE","T_SWITCH","T_CATCH","T_FOR"]:
                    if check_if_right_parentheses_after_token(tokens, curr_token_index, token):
                        break

                    else:
                        res["before"] += " "

    return res

def in_php_tags(tokens, curr_token_index, config):
    """Puts spaces within php with echo tags
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["<?= and ?>"] == "True":
        if tokens[curr_token_index] == "T_OPEN_TAG_WITH_ECHO":
            res["after"] += " "

        if tokens[curr_token_index] == "T_CLOSE_TAG":
            res["before"] += " "

    return res

#In ternary operator
def before_question(tokens, curr_token_index, config):
    """Puts space before ? in ternary operator
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["Before '?'"] == "True":
        if tokens[curr_token_index] == "Q_MARK":
            res["before"] += " "

    return res

def after_question(tokens, curr_token_index, config):
    """Puts space after ? in ternary operator
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["After '?'"] == "True":
        if tokens[curr_token_index] == "Q_MARK":
            res["after"] += " "

    return res

def before_colon_ternary(tokens, curr_token_index, config):
    """Puts space before : in ternary operator
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["Before ':'"] == "True":
        if check_if_colon_in_ternary(tokens, curr_token_index):
            res["before"] += " "

    return res

def after_colon_ternary(tokens, curr_token_index, config):
    """Puts space after : in ternary operator
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if config["Spaces"]["After ':'"] == "True":
        if check_if_colon_in_ternary(tokens, curr_token_index):
            res["after"] += " "

    return res

def between_question_and_colon(tokens, curr_token_index, config):
    """Puts space after between ?:
    if flag is set to True"""

    res = {"before": "", "after": ""}

    if curr_token_index - 1 == len(tokens):
        return res

    if config["Spaces"]["After '?'"] == "True":
        if tokens[curr_token_index] == "Q_MARK":
            if tokens[curr_token_index+1] == "COLON":
                res["after"] += " "

    return res