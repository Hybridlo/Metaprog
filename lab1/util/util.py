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

    curr_token = tokens[curr_token_index]
    prev_token = tokens[curr_token_index-1]

    if prev_token.position[0] < curr_token.position[0]:
        return True

    return False

def previous_token_is_semicolon(tokens, curr_token_index):
    """Check if last token was a semicolon"""

    prev_token = tokens[curr_token_index-1]

    if prev_token.token == "SEMICOLON":
        return True
    
    return False