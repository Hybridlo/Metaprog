def count_token_nesting(tokens, curr_token_index, nesting_token_open, nesting_token_close):
    """Helper function to count 
    nesting levels of specified tokens
    such as brackets, parenthesis
    and php tags"""

    nesting_level = 0
    
    for i in range(len(tokens)):
        

        if tokens[i] in nesting_token_open:
            nesting_level += 1

        if tokens[i] in nesting_token_close:
            nesting_level -= 1

        if i == curr_token_index:
            break

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

def continues_previous_line(tokens, curr_token_index):
    """Check this token continues a line"""
    if curr_token_index == 0:
        return False

    prev_token = tokens[curr_token_index-1]
    curr_token = tokens[curr_token_index]

    tokens_dont_continue = ["SEMICOLON", "T_TAG", "T_OPEN_TAG", "T_OPEN_TAG_WITH_ECHO", "R_PARENTHESES_OPEN", "S_PARENTHESES_OPEN",
                            "BRACKET_OPEN", "BRACKET_CLOSE", "T_COMMENT", "T_DOC_COMMENT",
                           ]

    #functions can be declared on newline after modifiers, doesn't count as continuation
    if prev_token not in tokens_dont_continue and curr_token != "T_FUNCTION":
        return True
    
    return False

def check_if_func_declared(tokens, curr_token_index):
    """Check if function is declared with current token;
    Function declaration defined as next token sequence:
    T_FUNCTION, T_STRING, R_PARENTHESES_OPEN"""

    if curr_token_index == 0 or len(tokens) == curr_token_index + 1:
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

    if curr_token_index == 0 or len(tokens) == curr_token_index + 1:
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
    if len(tokens) - 2 < curr_token_index:
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

def check_class_decl_left_brace(tokens, curr_token_index):
    """Check if current token is left brace and after class declaration;
    class declaration can have these tokens:
    T_STRING, COMMA, T_IMPLEMENTS, T_EXTENDS, T_CLASS"""
    if tokens[curr_token_index] != "BRACKET_OPEN":
        return False

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

def check_after_function_declaration(tokens, curr_token_index, needed_token):
    """Check current token and is after function declaration;
    function declaration can have these tokens:
    COLON, T_STRING, T_VARIABLE, COMMA, R_PARENTHESES_OPEN, R_PARENTHESES_CLOSE, T_FUNCTION,
    EQUAL, T_LNUMBER, T_DNUMBER"""
    if tokens[curr_token_index] != needed_token:
        return False

    i = curr_token_index - 1

    while True:
        if i < 0:
            return False

        if tokens[i] in ["COLON", "T_STRING", "T_VARIABLE", "COMMA", "R_PARENTHESES_OPEN",
                         "R_PARENTHESES_CLOSE", "EQUAL", "T_LNUMBER", "T_DNUMBER"]:
            i -= 1
            continue

        if tokens[i] == "T_FUNCTION":
            return True

        return False    #invalid token found

def check_left_brace_after_token(tokens, curr_token_index, needed_token):
    """Check if current token is left brace and after specified token;
    skips parentheses in between current and specified,
    and everything in these parentheses"""
    if tokens[curr_token_index] != "BRACKET_OPEN":
        return False

    i = curr_token_index - 1
    nesting = 0

    while True:
        if i < 1:
            return False

        if tokens[i] == "R_PARENTHESES_CLOSE":
            nesting += 1
        elif tokens[i] == "R_PARENTHESES_OPEN":
            nesting -= 1
        
        
        if nesting == 0:       #nesting == 0, current token at i must be the needed one
            return tokens[i] == needed_token

        i -= 1

def check_left_parentheses_after_func_decl(tokens, curr_token_index):
    """Check if current token is opening
    parentheses and after function declaration"""
    if curr_token_index == 0:
        return False

    if tokens[curr_token_index] != "R_PARENTHESES_OPEN":
        return False

    prev_token_1 = tokens[curr_token_index-1]
    prev_token_2 = tokens[curr_token_index-2]

    if prev_token_1 == "T_STRING" and prev_token_2 == "T_FUNCTION":
        return True

    return False

def check_right_parentheses_after_func_decl(tokens, curr_token_index):
    """Check if current token is closing
    parentheses and after function declaration;
    skips everything in these parentheses"""
    if tokens[curr_token_index] != "R_PARENTHESES_CLOSE":
        return False

    i = curr_token_index - 1
    nesting = 1

    while True:
        if i < 1:
            return False

        if tokens[i] == "R_PARENTHESES_CLOSE":
            nesting += 1
        elif tokens[i] == "R_PARENTHESES_OPEN":
            nesting -= 1
        
        
        if nesting == 0:       #nesting == 0, current token at i must be an idetifier string and the one before - T_FUNCTION
            return tokens[i] == "T_STRING" and tokens[i-1] == "T_FUNCTION"

        i -= 1

def check_if_left_parentheses_after_token(tokens, curr_token_index, needed_token):
    """Check if current token is opening
    parentheses and after specified token"""
    if curr_token_index == 0:
        return False

    if tokens[curr_token_index] != "R_PARENTHESES_OPEN":
        return False

    prev_token = tokens[curr_token_index-1]

    if prev_token == needed_token:
        return True

    return False

def check_if_right_parentheses_after_token(tokens, curr_token_index, needed_token):
    """Check if current token is closing
    parentheses and after specified token;
    skips everything in these parentheses"""
    if tokens[curr_token_index] != "R_PARENTHESES_CLOSE":
        return False

    i = curr_token_index - 1
    nesting = 1

    while True:
        if i < 0:
            return False

        if tokens[i] == "R_PARENTHESES_CLOSE":
            nesting += 1
        elif tokens[i] == "R_PARENTHESES_OPEN":
            nesting -= 1
        
        
        if nesting == 0:       #nesting == 0, current token at i must be the one searched for
            return tokens[i] == needed_token

        i -= 1

def check_if_colon_in_ternary(tokens, curr_token_index):
    """Check if current token is a colon in ternary operator"""
    if tokens[curr_token_index] != "COLON":
        return False

    i = curr_token_index - 1

    while True:
        if i < 0:
            return False

        if tokens[i] == "SEMICOLON":
            return False    #didn't find matching ?

        if tokens[i] == "Q_MARK":
            return True

        i -= 1

def check_semicolon_in_for(tokens, curr_token_index):
    """Check if current token is semicolon in for"""
    if tokens[curr_token_index] != "SEMICOLON":
        return False

    i = curr_token_index - 1
    nesting = 1

    while True:
        if i < 0:
            return False

        if tokens[i] == "R_PARENTHESES_CLOSE":
            nesting += 1
        elif tokens[i] == "R_PARENTHESES_OPEN":
            nesting -= 1
        
        
        if nesting == 0:       #nesting == 0, current token at i must be T_FOR
            return tokens[i] == "T_FOR"

        i -= 1

def check_type_cast(tokens, curr_token_index):
    """Check if token is type cast"""

    if tokens[curr_token_index] in ["T_ARRAY_CAST", "T_BOOL_CAST", "T_DOUBLE_CAST", "T_INT_CAST", "T_OBJECT_CAST", "T_STRING_CAST", "T_UNSET_CAST"]:
        return True

    if curr_token_index == 0 or len(tokens) == curr_token_index + 1:
        return False

    curr_token = tokens[curr_token_index]
    prev_token = tokens[curr_token_index-1]
    next_token = tokens[curr_token_index+1]

    if (curr_token == "T_STRING" and prev_token == "R_PARENTHESES_OPEN"
        and next_token == "R_PARENTHESES_CLOSE"):

        return True

    return False

def check_if_token_paired(tokens, curr_token_index, interest_token, pair_token, skip_tokens):
    """Checks if current token is the one needed and
    if it's paired with pair token, skipping blocks in {}
    and skip tokens (like catch in try-catch-finally)"""
    if tokens[curr_token_index] != interest_token:
        return False

    i = curr_token_index - 1
    nesting = 0

    while True:
        if i < 0:
            return False

        if tokens[i] == "BRACKET_CLOSE":
            nesting += 1
        elif tokens[i] == "BRACKET_OPEN":
            nesting -= 1
        
        #nesting == 0, current token at i must be opening second of pair; skip if token at i is skip token
        if nesting == 0 and not tokens[i] in skip_tokens:       
            return tokens[i] == pair_token

        i -= 1

def check_if_in_case_branch(tokens, curr_token_index):
    """Checks if token is in case branch, skipping {} blocks"""
    i = curr_token_index - 1
    nesting = 0

    while True:
        if i < 0:
            return False

        if tokens[i] == "BRACKET_CLOSE":
            nesting += 1
        elif tokens[i] == "BRACKET_OPEN":
            nesting -= 1

        if nesting == 0:       #nesting == 0, current token at i must be opening bracket
            return tokens[i] == "T_CASE"

        i -= 1

def check_mod_before_func_or_class(tokens, curr_token_index):
    if curr_token_index + 1 == len(tokens):
        return False

    modifier_list = ["T_PRIVATE", "T_PROTECTED", "T_PUBLIC", "T_ABSTRACT", "T_FINAL"]

    curr_token = tokens[curr_token_index]
    next_token = tokens[curr_token_index+1]

    if curr_token in modifier_list and next_token in ["T_FUNCTION", "T_CLASS"]:
        return True

    return False

def check_string_after_var(tokens, curr_token_index):
    if len(tokens) == curr_token_index + 1:
        return False

    curr_token = tokens[curr_token_index]
    next_token = tokens[curr_token_index+1]

    if curr_token == "T_STRING" and next_token == "T_VARIABLE":
        return True

    return False

def check_class_decl_right_brace(tokens, curr_token_index):
    """checks for closing bracket that is part
    of class declaration"""

    if tokens[curr_token_index] != "BRACKET_CLOSE":
        return False

    i = curr_token_index - 1
    nesting = 1

    while True:
        if i < 0:
            return False

        if tokens[i] == "BRACKET_CLOSE":
            nesting += 1
        elif tokens[i] == "BRACKET_OPEN":
            nesting -= 1

        if nesting == 0:       #nesting == 0, current token at i must be opening bracket
            return check_class_decl_left_brace(tokens, i)

        i -= 1

def check_end_of_keyword(tokens, curr_token_index, keyword_token):
    """Check if current token ends keyword line"""
    if tokens[curr_token_index] != "SEMICOLON":
        return False

    i = curr_token_index - 1

    while True:
        if i < 0:
            return False

        if tokens[i] == "SEMICOLON":
            return False

        elif tokens[i] == keyword_token:       #found keyword on this line
            return True

        i -= 1

def check_in_block(tokens, curr_token_index, block_keyword, start_nesting=1):
    """checks if current token is in specified keyword block
    start_nesting is used for checking class method with value of 2"""

    i = curr_token_index
    nesting = start_nesting

    while True:
        if i < 0:
            return False

        if tokens[i] == "BRACKET_CLOSE":
            nesting += 1
        elif tokens[i] == "BRACKET_OPEN":
            nesting -= 1

        if nesting == 0:       #nesting == 0, current token at i must be opening bracket
            if block_keyword == "T_FUNCTION":
                return check_after_function_declaration(tokens, i, "BRACKET_OPEN")

            if block_keyword == "T_CLASS":
                return check_class_decl_left_brace(tokens, i)

            return False

        i -= 1

def check_func_right_brace(tokens, curr_token_index):
    """checks for closing bracket that is part
    of function declaration"""

    if tokens[curr_token_index] != "BRACKET_CLOSE":
        return False

    i = curr_token_index - 1
    nesting = 1

    while True:
        if i < 0:
            return False

        if tokens[i] == "BRACKET_CLOSE":
            nesting += 1
        elif tokens[i] == "BRACKET_OPEN":
            nesting -= 1

        if nesting == 0:       #nesting == 0, current token must be opening bracket before function decl
            return check_after_function_declaration(tokens, i, "BRACKET_OPEN")

        i -= 1