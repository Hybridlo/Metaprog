from util.util import *
from functools import partial

#Indents formatters
def apply_indent(tokens, curr_token_index, config):
    """Applies indent specified in config"""
    res = {"spaces_before": 0, "spaces_after": 0}

    indent = int(config["Indents"]["Indent"])

    if indent != 0 and check_if_first_token_in_line(tokens, curr_token_index):
        nesting_level = count_token_nesting(tokens, curr_token_index, ["BRACKET_OPEN"], ["BRACKET_CLOSE"])

        res["spaces_before"] += indent * nesting_level
    
    return res

def apply_continue_indent(tokens, curr_token_index, config):
    """Applies continuation indent specified in config"""

    res = {"spaces_before": 0, "spaces_after": 0}

    cont_indent = int(config["Indents"]["Continuation indent"])

    if (cont_indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
        and continues_previous_line(tokens, curr_token_index)):

        res["spaces_before"] += cont_indent

    return res

def apply_indent_in_php_tags(tokens, curr_token_index, config):
    """Applies indent specified in configs
    if php tags indent flag is set to True"""
    res = {"spaces_before": 0, "spaces_after": 0}

    indent = int(config["Indents"]["Indent"])

    if (indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
        and config["Indents"]["Indent code in PHP tags"] == "True"):

        nesting_level = count_token_nesting(tokens, curr_token_index, ["T_OPEN_TAG", "T_OPEN_TAG_WITH_ECHO"], ["T_CLOSE_TAG"])

        res["spaces_before"] += indent * nesting_level

    return res

#Spaces before parentheses formatters
def func_decl_parentheses(tokens, curr_token_index, config):
    """Puts space between function declaration
    and paretheses if flag set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"]["Function declaration parentheses"] == "True"
        and check_if_func_declared(tokens, curr_token_index)):

        res["spaces_after"] += 1

    return res

def func_call_parentheses(tokens, curr_token_index, config):
    """Puts space between function call
    and paretheses if flag set to True"""
    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"]["Function call parentheses"] == "True"
        and check_if_func_call(tokens, curr_token_index)):

        res["spaces_after"] += 1

    return res

def _token_and_parentheses(config_key, interest_token, tokens, curr_token_index, config):
    """Puts space between token of interest 
    and paretheses if flag in config_key is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"][config_key] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, interest_token)):

        res["spaces_after"] += 1

    return res

anon_func_paretheses = partial(_token_and_parentheses, "Anonymous function parentheses", "T_FUNCTION")
if_parentheses = partial(_token_and_parentheses, "'if' parentheses", "T_IF")
for_parentheses = partial(_token_and_parentheses, "'for' parentheses", "T_FOR")
foreach_parentheses = partial(_token_and_parentheses, "'for' parentheses", "T_FOREACH")     #shared rule
while_parentheses = partial(_token_and_parentheses, "'while' parentheses", "T_WHILE")
switch_parentheses = partial(_token_and_parentheses, "'switch' parentheses", "T_SWITCH")
catch_parentheses = partial(_token_and_parentheses, "'catch' parentheses", "T_CATCH")
array_init_parentheses = partial(_token_and_parentheses, "Array initializer parentheses", "T_ARRAY")

#Spaces around operators
def _around_token(config_key, interest_tokens, tokens, curr_token_index, config):
    """Puts spaces around token of interest 
    if flag in config_key is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"][config_key] == "True" and tokens[curr_token_index] in interest_tokens:
        res["spaces_after"] += 1
        res["spaces_before"] += 1

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

def assignment_in_declare(tokens, curr_token_index, config):
    """Puts spaces around assignment in declare construct 
    if flag in config_key is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"]["Assignment in declare statement"] == "True" 
        and check_assign_in_declare(tokens, curr_token_index)):
        res["spaces_after"] += 1
        res["spaces_before"] += 1

    return res

#Space before left brace
def class_declaration_left_brace(tokens, curr_token_index, config):
    """Puts space before left brace in class declaration
    if flag in config_key is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"]["Class left brace"] == "True" 
        and check_class_declaration(tokens, curr_token_index)):
        res["spaces_before"] += 1

    return res

def func_declaration_left_brace(tokens, curr_token_index, config):
    """Puts space before left brace in function declaration
    if flag in config_key is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"]["Function left brace"] == "True" 
        and check_after_function_declaration(tokens, curr_token_index, "BRACKET_OPEN")):
        res["spaces_before"] += 1

    return res

def _left_brace_after_token(config_key, interest_token, tokens, curr_token_index, config):
    """Puts space before left brace
    that follows interest_token and
    if flag in config_key is set to True;
    this function skips some other tokens in between"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"][config_key] == "True" 
        and check_left_brace_after_token(tokens, curr_token_index, interest_token)):

        res["spaces_before"] += 1

    return res

if_left_brace = partial(_left_brace_after_token, "'if' left brace", "T_IF")
else_left_brace = partial(_left_brace_after_token, "'else' left brace", "T_ELSE")
elseif_left_brace = partial(_left_brace_after_token, "'else' left brace", "T_ELSEIF")     #share one rule
for_left_brace = partial(_left_brace_after_token, "'for' left brace", "T_FOR")
foreach_left_brace = partial(_left_brace_after_token, "'for' left brace", "T_FOREACH")    #share one rule
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

    res = {"spaces_before": 0, "spaces_after": 0}

    if (config["Spaces"][config_key] == "True" and tokens[curr_token_index] == interest_token):
        res["spaces_before"] += 1

    return res


before_else = partial(_before_token, "'else' keyword", "T_ELSE")
before_while = partial(_before_token, "'while' keyword", "T_WHILE")
before_catch = partial(_before_token, "'catch' keyword", "T_CATCH")
before_finally = partial(_before_token, "'finally' keyword", "T_FINALLY")

#Spaces within
def in_brackets(tokens, curr_token_index, config):
    """Puts spaces within brackets
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Brackets"] == "True":
        if tokens[curr_token_index] == "S_PARENTHESES_OPEN":
            res["spaces_after"] += 1

        if tokens[curr_token_index] == "S_PARENTHESES_CLOSE":
            res["spaces_before"] += 1

    return res

def in_func_decl_parentheses(tokens, curr_token_index, config):
    """Puts spaces within function declaration parantheses
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Within function declaration parentheses"] == "True":
        if check_left_parentheses_after_func_decl(tokens, curr_token_index):
            res["spaces_after"] += 1

        if check_right_parentheses_after_func_decl(tokens, curr_token_index):
            res["spaces_before"] += 1

    return res

def _in_token_parentheses(config_key, interest_token, tokens, curr_token_index, config):
    """Puts spaces within arguments
    parantheses of specified token
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"][config_key] == "True":
        if check_if_left_parentheses_after_token(tokens, curr_token_index, interest_token):
            res["spaces_after"] += 1

        if check_if_right_parentheses_after_token(tokens, curr_token_index, interest_token):
            res["spaces_before"] += 1

    return res

in_array_init_parentheses = partial(_in_token_parentheses, "Within array initializer parentheses", "T_ARRAY")
in_func_call_parentheses = partial(_in_token_parentheses, "Within array initializer parentheses", "T_STRING")
in_if_parentheses = partial(_in_token_parentheses, "Within 'if' parentheses", "T_IF")
in_for_parentheses = partial(_in_token_parentheses, "Within 'for' parentheses", "T_FOR")
in_foreach_parentheses = partial(_in_token_parentheses, "Within 'for' parentheses", "T_FOREACH")    #share one rule
in_while_parentheses = partial(_in_token_parentheses, "Within 'while' parentheses", "T_WHILE")
in_switch_parentheses = partial(_in_token_parentheses, "Within 'switch' parentheses", "T_SWITCH")
in_catch_parentheses = partial(_in_token_parentheses, "Within 'catch' parentheses", "T_CATCH")

def in_grouping_parentheses(tokens, curr_token_index, config):
    """Puts spaces within parantheses that aren't any of the above
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Grouping parentheses"] == "True":
        if tokens[curr_token_index] == "R_PARENTHESES_OPEN":
            if not check_left_parentheses_after_func_decl(tokens, curr_token_index):
                for token in ["T_ARRAY","T_STRING","T_IF","T_WHILE","T_SWITCH","T_CATCH","T_FOR"]:
                    if check_if_left_parentheses_after_token(tokens, curr_token_index, token):
                        break

                    else:
                        res["spaces_after"] += 1

        if tokens[curr_token_index] == "R_PARENTHESES_CLOSE":
            if not check_right_parentheses_after_func_decl(tokens, curr_token_index):
                for token in ["T_ARRAY","T_STRING","T_IF","T_WHILE","T_SWITCH","T_CATCH","T_FOR"]:
                    if check_if_right_parentheses_after_token(tokens, curr_token_index, token):
                        break

                    else:
                        res["spaces_before"] += 1

    return res

def in_php_tags(tokens, curr_token_index, config):
    """Puts spaces within php with echo tags
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["<?= and ?>"] == "True":
        if tokens[curr_token_index] == "T_OPEN_TAG_WITH_ECHO":
            res["spaces_after"] += 1

        if tokens[curr_token_index] == "T_CLOSE_TAG":
            res["spaces_before"] += 1

    return res

#Spaces in ternary operator
def before_question(tokens, curr_token_index, config):
    """Puts space before ? in ternary operator
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Before '?'"] == "True":
        if tokens[curr_token_index] == "Q_MARK":
            res["spaces_before"] += 1

    return res

def after_question(tokens, curr_token_index, config):
    """Puts space after ? in ternary operator
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After '?'"] == "True":
        if tokens[curr_token_index] == "Q_MARK":
            res["spaces_after"] += 1

    return res

def before_colon_ternary(tokens, curr_token_index, config):
    """Puts space before : in ternary operator
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Before ':'"] == "True":
        if check_if_colon_in_ternary(tokens, curr_token_index):
            res["spaces_before"] += 1

    return res

def after_colon_ternary(tokens, curr_token_index, config):
    """Puts space after : in ternary operator
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After ':'"] == "True":
        if check_if_colon_in_ternary(tokens, curr_token_index):
            res["spaces_after"] += 1

    return res

def between_question_and_colon(tokens, curr_token_index, config):
    """Puts space after between ?:
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if curr_token_index - 1 == len(tokens):
        return res

    if config["Spaces"]["After '?'"] == "True":
        if tokens[curr_token_index] == "Q_MARK":
            if tokens[curr_token_index+1] == "COLON":
                res["spaces_after"] += 1

    return res

#Other spaces
def before_comma(tokens, curr_token_index, config):
    """Puts space before ,
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Before comma"] == "True":
        if tokens[curr_token_index] == "COMMA":
            res["spaces_before"] += 1

    return res

def after_comma(tokens, curr_token_index, config):
    """Puts space before ,
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After comma"] == "True":
        if tokens[curr_token_index] == "COMMA":
            res["spaces_after"] += 1

    return res

def before_for_semicolon(tokens, curr_token_index, config):
    """Puts space before ; in for
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Before 'for' semicolon"] == "True":
        if check_semicolon_in_for(tokens, curr_token_index):
            res["spaces_before"] += 1

    return res

def after_for_semicolon(tokens, curr_token_index, config):
    """Puts space after ; in for
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After 'for' semicolon"] == "True":
        if check_semicolon_in_for(tokens, curr_token_index):
            res["spaces_after"] += 1

    return res

def after_type_cast(tokens, curr_token_index, config):
    """Puts space after type cast
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After type cast"] == "True":
        if check_type_cast(tokens, curr_token_index):
            res["spaces_after"] += 1

    return res

def before_return_type_colon(tokens, curr_token_index, config):
    """Puts space before return type colon
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Before colon in return type"] == "True":
        if check_after_function_declaration(tokens, curr_token_index, "COLON"):
            res["spaces_before"] += 1

    return res

def after_return_type_colon(tokens, curr_token_index, config):
    """Puts space after return type colon
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After colon in return type"] == "True":
        if check_after_function_declaration(tokens, curr_token_index, "COLON"):
            res["spaces_after"] += 1

    return res

def before_unary_not(tokens, curr_token_index, config):
    """Puts space before !
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["Before unary Not (!)"] == "True":
        if tokens[curr_token_index] == "EX_MARK":
            res["spaces_before"] += 1

    return res

def after_unary_not(tokens, curr_token_index, config):
    """Puts space after !
    if flag is set to True"""

    res = {"spaces_before": 0, "spaces_after": 0}

    if config["Spaces"]["After unary Not (!)"] == "True":
        if tokens[curr_token_index] == "EX_MARK":
            res["spaces_after"] += 1

    return res

#Wrapping
def one_line_control_statement(tokens, curr_token_index, config):
    """Puts control statement in one line
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"]["Control statement in one line"] == "False":
        if check_if_right_parentheses_after_token(tokens, curr_token_index, "T_IF"):
            res["newlines_after"] += 1

    return res

#Function declaration wrapping
def func_decl_newline_after_left_parentheses(tokens, curr_token_index, config):
    """Puts newline in function
    declaration after left parentheses
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"]["Declatarion new line after '('"] == "True":
        if check_left_parentheses_after_func_decl(tokens, curr_token_index):
            res["newlines_after"] += 1

    return res

def func_decl_newline_before_right_parentheses(tokens, curr_token_index, config):
    """Puts newline in function
    declaration before right parentheses
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"]["Declatarion place ')' on new line"] == "True":
        if check_right_parentheses_after_func_decl(tokens, curr_token_index):
            res["newlines_before"] += 1

    return res

def func_decl_newline_after_right_parentheses(tokens, curr_token_index, config):
    """Puts newline in function
    declaration after right parentheses
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"]["Keep ')' and '{' on one line"] == "False":
        if check_right_parentheses_after_func_decl(tokens, curr_token_index):
            res["newlines_after"] += 1

    return res

#Function and keywords call wrapping
def _newline_after_left_parentheses_after_token(config_key, interest_token, tokens, curr_token_index, config):
    """Puts newline after left parentheses
    if it's after specified token
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"][config_key] == "True":
        if check_if_left_parentheses_after_token(tokens, curr_token_index, interest_token):
            res["newlines_after"] += 1

    return res

def _newline_before_right_parentheses_after_token(config_key, interest_token, tokens, curr_token_index, config):
    """Puts newline before right parentheses
    if it's after specified token
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"][config_key] == "True":
        if check_if_right_parentheses_after_token(tokens, curr_token_index, interest_token):
            res["newlines_before"] += 1

    return res

func_call_newline_left_parentheses = partial(_newline_after_left_parentheses_after_token, "Call new line after '('", "T_STRING")
if_newline_left_parentheses = partial(_newline_after_left_parentheses_after_token, "If() new line after '('", "T_IF")
for_newline_left_parentheses = partial(_newline_after_left_parentheses_after_token, "For() new line after '('", "T_FOR")
foreach_newline_left_parentheses = partial(_newline_after_left_parentheses_after_token, "For() new line after '('", "T_FOREACH")        #share one rule
array_newline_left_init_parentheses = partial(_newline_after_left_parentheses_after_token, "New line after '('", "T_ARRAY")

func_call_newline_right_parentheses = partial(_newline_before_right_parentheses_after_token, "Call place ')' on new line", "T_STRING")
if_newline_right_parentheses = partial(_newline_before_right_parentheses_after_token, "If() place ')' on new line", "T_IF")
for_newline_right_parentheses = partial(_newline_before_right_parentheses_after_token, "For() place ')' on new line", "T_FOR")
foreach_newline_right_parentheses = partial(_newline_before_right_parentheses_after_token, "For() place ')' on new line", "T_FOREACH")  #share one rule
array_newline_right_init_parentheses = partial(_newline_before_right_parentheses_after_token, "Place ')' on new line", "T_ARRAY")

def _newline_before_paired_token(config_key, interest_token, pair_token, skip_tokens, tokens, curr_token_index, config):
    """Puts newline before specified token
    if it's paired (after '}' and another token)
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"][config_key] == "True":
        if check_if_token_paired(tokens, curr_token_index, interest_token, pair_token, skip_tokens):
            res["newlines_before"] += 1

    return res

else_newline = partial(_newline_before_paired_token, "'else' on new line", "T_ELSE", "T_IF", ["T_ELSEIF"])
elseif_newline = partial(_newline_before_paired_token, "'else' on new line", "T_ELSEIF", "T_IF", ["T_ELSEIF"])    #shared rule
while_newline = partial(_newline_before_paired_token, "'while' on new line", "T_WHILE", "T_DO", [])
catch_newline = partial(_newline_before_paired_token, "'catch' on new line", "T_CATCH", "T_TRY", [])
finally_newline = partial(_newline_before_paired_token, "'finally' on new line", "T_FINALLY", "T_TRY", ["T_CATCH"])

#Switch indentation
def indent_case_branches(tokens, curr_token_index, config):
    """Removes one indentation level from case branches
    if flag for indenting case branches id set to False"""

    res = {"spaces_before": 0, "spaces_after": 0}

    indent = int(config["Indents"]["Indent"])

    if config["Wrapping and Braces"]["Indent 'case' branches"] == "False":
        if (indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
            and check_if_in_case_branch(tokens, curr_token_index) and tokens[curr_token_index] != "T_BREAK"):
            
            res["spaces_before"] -= indent
    
    return res

def indent_break_case_branches(tokens, curr_token_index, config):
    """Removes one indentation level from break in case branches
    if flag for indenting case branches id set to False (separate rule)"""

    res = {"spaces_before": 0, "spaces_after": 0}

    indent = int(config["Indents"]["Indent"])

    if config["Wrapping and Braces"]["Indent 'break' from 'case'"] == "False":
        if (indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
            and check_if_in_case_branch(tokens, curr_token_index) and tokens[curr_token_index] == "T_BREAK"):
            
            res["spaces_before"] -= indent
    
    return res

#Modifier wrap
def wrap_after_mods_list(tokens, curr_token_index, config):
    """Puts newline after modifier list
    if flag is set to True"""

    res = {"newlines_before": 0, "newlines_after": 0}

    if config["Wrapping and Braces"]["Wrap after modifier list"] == "True":
        if check_func_or_class_with_mods(tokens, curr_token_index):
            res["newlines_before"] += 1

    return res

#additional general rule(s)
def newline_after_tokens(tokens, curr_token_index, config):
    """Puts newline at the end of some tokens if it's not in for loop"""

    newline_tokens = ["SEMICOLON", "T_OPEN_TAG", "T_OPEN_TAG_WITH_ECHO", "BRACKET_OPEN", "BRACKET_CLOSE"]

    res = {"newlines_before": 0, "newlines_after": 0}

    if tokens[curr_token_index] in newline_tokens and not check_semicolon_in_for(tokens, curr_token_index):
        res["newlines_after"] += 1

    return res

def space_after_tokens(tokens, curr_token_index, config):
    """Puts space at the end of some tokens"""

    space_tokens_after = ["T_RETURN", "T_YIELD", "T_AS", "T_NAMESPACE", "T_REQUIRE", "T_NEW"]
    space_tokens_before = ["T_AS"]

    res = {"spaces_before": 0, "spaces_after": 0}

    if tokens[curr_token_index] in space_tokens_after:
        res["spaces_after"] += 1

    if tokens[curr_token_index] in space_tokens_before:
        res["spaces_before"] += 1

    return res

all_formatters = [
    apply_indent,
    apply_continue_indent,
    apply_indent_in_php_tags,
    func_decl_parentheses,
    func_call_parentheses,
    anon_func_paretheses,
    if_parentheses,
    for_parentheses,
    foreach_parentheses,
    while_parentheses,
    switch_parentheses,
    catch_parentheses,
    array_init_parentheses,

    assign_operators,
    logical_operators,
    equality_operators,
    relational_operators,
    bitwise_operators,
    additive_operators,
    multiplicative_operators,
    shift_operators,
    unary_operators,
    concat_operator,
    obj_access_operator,
    null_coal_operator,
    assignment_in_declare,

    class_declaration_left_brace,
    func_declaration_left_brace,
    if_left_brace,
    else_left_brace,
    elseif_left_brace,
    for_left_brace,
    foreach_left_brace,
    while_left_brace,
    do_left_brace,
    switch_left_brace,
    try_left_brace,
    catch_left_brace,
    finally_left_brace,

    before_else,
    before_while,
    before_catch,
    before_finally,

    in_brackets,
    in_func_decl_parentheses,
    in_array_init_parentheses,
    in_func_call_parentheses,
    in_if_parentheses,
    in_for_parentheses,
    in_foreach_parentheses,
    in_while_parentheses,
    in_switch_parentheses,
    in_catch_parentheses,
    in_grouping_parentheses,
    in_php_tags,

    before_question,
    after_question,
    before_colon_ternary,
    after_colon_ternary,
    between_question_and_colon,

    before_comma,
    after_comma,
    before_for_semicolon,
    after_for_semicolon,
    after_type_cast,
    before_return_type_colon,
    after_return_type_colon,
    before_unary_not,
    after_unary_not,
    
    one_line_control_statement,

    func_decl_newline_after_left_parentheses,
    func_decl_newline_before_right_parentheses,
    func_decl_newline_after_right_parentheses,

    func_call_newline_left_parentheses,
    func_call_newline_right_parentheses,

    if_newline_left_parentheses,
    if_newline_right_parentheses,
    else_newline,

    for_newline_left_parentheses,
    foreach_newline_left_parentheses,
    for_newline_right_parentheses,
    foreach_newline_right_parentheses,

    while_newline,

    indent_case_branches,
    indent_break_case_branches,

    catch_newline,
    finally_newline,

    array_newline_left_init_parentheses,
    array_newline_right_init_parentheses,

    wrap_after_mods_list,

    newline_after_tokens,
    space_after_tokens,
]