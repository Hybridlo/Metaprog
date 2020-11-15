from util.util import *

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

def anon_func_paretheses(tokens, curr_token_index, config):
    """Puts space between anonymous function call
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["Anonymous function parenteses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_FUNCTION")):

        res["after"] += " "

    return res

def if_parentheses(tokens, curr_token_index, config):
    """Puts space between 'if' statement
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["'if' parenteses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_IF")):

        res["after"] += " "

    return res

def for_parentheses(tokens, curr_token_index, config):
    """Puts space between 'for' statement
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["'for' parenteses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_FOR")):

        res["after"] += " "

    return res

def while_paretheses(tokens, curr_token_index, config):
    """Puts space between 'while' statement
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["'while' parenteses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_WHILE")):

        res["after"] += " "

    return res

def switch_paretheses(tokens, curr_token_index, config):
    """Puts space between 'switch' statement
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["'switch' parenteses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_SWITCH")):

        res["after"] += " "

    return res

def catch_paretheses(tokens, curr_token_index, config):
    """Puts space between 'catch' statement
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["'catch' parenteses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_CATCH")):

        res["after"] += " "

    return res

def array_init_paretheses(tokens, curr_token_index, config):
    """Puts space between array initializer
    and paretheses if flag set to True"""

    res = {"before": "", "after": ""}

    if (config["Spaces"]["Array initializer parentheses"] == "True"
        and check_if_token_before_paretheses(tokens, curr_token_index, "T_ARRAY")):

        res["after"] += " "

    return res