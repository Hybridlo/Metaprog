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
    """Check if function is declared with current token;
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
    """Check if function is called with current token;
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

def check_assign_in_declare(tokens, curr_token_index):
    """Check if current token is assignment
    in declare construct; defined as next token sequence:
    T_DECLARE, R_PARENTHESES_OPEN, T_STRING, EQUAL"""

    if curr_token_index < 3:
        return False

    curr_token = tokens[curr_token_index]
    prev_token_1 = tokens[curr_token_index-1]
    prev_token_2 = tokens[curr_token_index-2]
    prev_token_3 = tokens[curr_token_index-3]

    if (prev_token_3 == "T_DECLARE" and prev_token_2 == "R_PARENTHESES_OPEN"
        and prev_token_1 == "T_STRING" and curr_token == "EQUAL"):

        return True

    return False

def check_class_declaration(tokens, curr_token_index):
    """Check if current token is after class declaration;
    class declaration can have these tokens:
    T_STRING, COMMA, T_IMPLEMENTS, T_EXTENDS, T_CLASS"""
    i = curr_token_index - 1

    while True:
        if i < 0:
            return False

        if tokens[i] in ["T_STRING", "COMMA", "T_IMPLEMENTS", "T_EXTENDS"]:
            i -= 1
            continue

        if tokens[i] == "T_CLASS":
            return True

        return False    #invalid token found

def check_function_declaration(tokens, curr_token_index):
    """Check if current token is after function declaration;
    function declaration can have these tokens:
    T_STRING, T_VARIABLE, COMMA, R_PARENTHESES_OPEN, R_PARENTHESES_CLOSE, T_FUNCTION"""
    i = curr_token_index - 1

    while True:
        if i < 0:
            return False

        if tokens[i] in ["T_STRING", "T_VARIABLE", "COMMA", "R_PARENTHESES_OPEN", "R_PARENTHESES_CLOSE"]:
            i -= 1
            continue

        if tokens[i] == "T_FUNCTION":
            return True

        return False    #invalid token found

def check_left_brace_after_token(tokens, curr_token_index, needed_token):
    """Check if current token is after specified;
    skips parentheses in between current and specified,
    and everything in these parentheses"""
    i = curr_token_index - 1
    nesting = 0

    while True:
        if i < 0:
            return False

        if tokens[i] == "R_PARENTHESES_CLOSE":
            nesting += 1
            i -= 1
            continue
        elif tokens[i] == "R_PARENTHESES_OPEN":
            nesting -= 1
            i -= 1
            continue
        elif nesting > 0:
            i -= 1
            continue

        elif tokens[i] == needed_token:
            return True

        return False    #invalid token found with parentheses closed