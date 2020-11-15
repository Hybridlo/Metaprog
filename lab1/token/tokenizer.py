from .tokens import detect_token
import time

class Token:
    """A class to hold token information"""

    def __init__(self, token, in_code, position):
        """
        token: string with a token, gotten from
        tokens dictionary in tokens.py

        in_code: string that keeps text, that
        generated the token

        position: tuple of ints, keeps the
        position of token in code
        """
        self.token = token
        self.in_code = in_code
        self.position = position

def check_whitespace(to_check):
    """function to check for whitespace"""
    if to_check in [" ", "\t", "\r"]:
        return True

    return False

def check_newline(to_check):
    """function to check for new line"""
    if to_check == "\n":
        return True

    return False

def scan_newlines_in_token(to_check):       #account for newlines in comments and strings
    amount = 0

    for letter in to_check:
        if check_newline(letter):
            amount += 1

    return amount

def check_parenteses(to_check, counters):
    """function to track parenteses"""
    if to_check == "(":
        counters["round"] += 1

    elif to_check == ")":
        counters["round"] -= 1

    elif to_check == "[":
        counters["square"] += 1

    elif to_check == "]":
        counters["square"] -= 1

    elif to_check == "{":
        counters["square"] += 1

    elif to_check == "}":
        counters["square"] -= 1

def tokenize(file_str):
    """
    tokenizer function
    
    file_str: string with file content
    that needs to be tokenizer

    returns: list of Tokens
    """

    res_tokens = []
    errors = []

    position = [1, 1]
    counters = {"round": 0, "square": 0, "braces": 0}

    while len(file_str) > 0:
        i = 0
        found_true = None
        found_true_str = ""

        while True:         #token extraction logic, ends when token is found or whitespace cleared
            i += 1
            str_to_take = file_str[:i]

            if len(str_to_take) < 2:        #next checks are irrelevant if len(str_to_take) >= 2
                if check_whitespace(str_to_take):       #if whitespace, skip it
                    file_str = file_str[i:]
                    position[1] += 1
                    break

            if check_newline(str_to_take):          #if newline - account for position and skip
                file_str = file_str[i:]
                position[0] += 1
                position[1] = 1
                break

            res = detect_token(str_to_take)

            if len(res["true"]) > 1:
                errors.append(f"Unidentified token at ({position[0]}, {position[1]})")
                file_str = file_str[len(str_to_take):]              #discard unidentified token
                break


            elif len(res["true"]) == 1:
                if len(res["none"]) == 0:       #case - 1 full token match, no possible other matches
                    res_tokens.append(Token(res["true"][0], str_to_take, tuple(position)))
                    position[1] += len(str_to_take)
                    file_str = file_str[len(str_to_take):]

                    check_parenteses(str_to_take, counters)

                    shift = scan_newlines_in_token(str_to_take)
                    if shift > 0:
                        position[0] += shift
                        position[1] = 1

                    break

                else:           #case - 1 full token match, but may match another token, if scanned more
                    found_true = res["true"][0]
                    found_true_str = str_to_take
                    continue

            else:
                if len(res["none"]) > 0:        #case - no full token match, but there are candidates
                    continue

                else:           #case - no full token match and no candidates
                    if found_true != None:      #use previous full match if available
                        res_tokens.append(Token(found_true, found_true_str, tuple(position)))
                        position[1] += len(found_true_str)
                        file_str = file_str[len(found_true_str):]

                        check_parenteses(found_true_str, counters)

                        shift = scan_newlines_in_token(str_to_take)
                        if shift > 0:
                            position[0] += shift
                            position[1] = 1

                        break

                    print("lal")
                    print(str_to_take)
                    errors.append(f"Unidentified token at ({position[0]}, {position[1]})")
                    file_str = file_str[len(str_to_take)-1:]        #discard unidentified token
                    break

    for key in counters:
        if counters[key] != 0:
            errors.append("Unclosed brakets/parenteses found")
            break

    return res_tokens, errors