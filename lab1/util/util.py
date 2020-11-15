def count_token_nesting(tokens, curr_token_index, nesting_token_open, nesting_token_close):
    """Helper function to count 
    nesting levels of specified tokens
    such as brackets, parenthesis
    and php tags"""

    nesting_level = 0

    for token in tokens:
        if tokens.index(token) == curr_token_index:
            break

        if token.token in nesting_token_open:
            nesting_level += 1

        if token.token in nesting_token_close:
            nesting_level -= 1

    return nesting_level

def check_if_first_token_in_line(tokens, curr_token_index):
    """Checks if specified token is placed first in line"""
    if curr_token_index == 0:
        return True

    curr_token = tokens[curr_token_index]
    prev_token = tokens[curr_token_index-1]

    if prev_token.position[0] < curr_token.position[0]:
        return True

    return False

def previous_token_is_semicolon(tokens, curr_token_index):
    """Check if last token was a semicolon"""
    if curr_token_index == 0:
        return False

    prev_token = tokens[curr_token_index-1]

    if prev_token.token == "SEMICOLON":
        return True
    
    return False

def check_if_func_declared(tokens, curr_token_index):
    """Check if function is declared with current token
    Function declaration defined as next token sequence:
    T_FUNCTION, T_STRING, R_PARENTHESES_OPEN"""

    if curr_token_index == 0 or len(tokens) == curr_token_index - 1:
        return False

    curr_token = tokens[curr_token_index]
    prev_token = tokens[curr_token_index-1]
    next_token = tokens[curr_token_index+1]

    if (curr_token == "T_STRING" and prev_token == "T_FUNCTION"
        and next_token == "R_PARENTHESES_OPEN"):

        return True

    return False

def check_if_func_call(tokens, curr_token_index):
    """Check if function is called with current token
    Function call defined as next token sequence:
    not T_FUNCTION, T_STRING, R_PARENTHESES_OPEN"""

    if curr_token_index == 0 or len(tokens) == curr_token_index - 1:
        return False

    curr_token = tokens[curr_token_index]
    next_token = tokens[curr_token_index+1]
    prev_token = tokens[curr_token_index-1]

    if (curr_token == "T_STRING" and prev_token != "T_FUNCTION"
        and next_token == "R_PARENTHESES_OPEN"):

        return True

    return False

def check_if_token_before_paretheses(tokens, curr_token_index, needed_token):
    """Check if current token is needed_token
    and is followed by paretheses"""
    if len(tokens) == curr_token_index - 1:
        return False

    curr_token = tokens[curr_token_index]
    next_token = tokens[curr_token_index+1]

    if curr_token == needed_token and next_token != "R_PARENTHESES_OPEN":
        return True

    return False