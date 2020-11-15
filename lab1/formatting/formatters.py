from util.util import *

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
    if php tags indent flag is set to true"""
    res = {"before": "", "after": ""}

    indent = int(config["Indents"]["Indent"])

    if (indent != 0 and check_if_first_token_in_line(tokens, curr_token_index)
        and config["Indents"]["Indent code in PHP tags"] == "True"):

        nesting_level = count_token_nesting(tokens, curr_token_index, ["T_OPEN_TAG", "T_OPEN_TAG_WITH_ECHO"], ["T_CLOSE_TAG"])

        res["before"] += " " * indent * nesting_level

    return res