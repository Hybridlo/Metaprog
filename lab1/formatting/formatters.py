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

def token_and_parentheses(config_key, interest_token, tokens, curr_token_index, config):
    """Puts space between token of interest 
    and paretheses if flag in config_key is set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"][config_key] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, interest_token)):

        res["after"] += " "

    return res

anon_func_paretheses = partial(token_and_parentheses, "Anonymous function parenteses", "T_FUNCTION")
if_parentheses = partial(token_and_parentheses, "'if' parenteses", "T_IF")
for_parentheses = partial(token_and_parentheses, "'for' parenteses", "T_FOR")
while_parentheses = partial(token_and_parentheses, "'while' parenteses", "T_WHILE")
switch_parentheses = partial(token_and_parentheses, "'switch' parenteses", "T_SWITCH")
catch_parentheses = partial(token_and_parentheses, "'catch' parenteses", "T_CATCH")
array_init_paretheses = partial(token_and_parentheses, "Array initializer parentheses", "T_ARRAY")