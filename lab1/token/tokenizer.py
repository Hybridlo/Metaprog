from .tokens import detect_token

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

def tokenize(file_str):
    """
    tokenizer function
    
    file_str: string with file content
    that needs to be tokenizer

    returns: list of Tokens
    """

    res_tokens = []

    position = [1, 1]

    while len(file_str) > 0:
        i = 0
        found_true = None
        found_true_str = ""

        while True:         #token extraction logic, ends when token is found or whitespace cleared
            i += 1
            str_to_take = file_str[:i]
            print(file_str)

            if len(str_to_take) < 2:        #next check are irrelevant if len(str_to_take) >= 2
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
                raise Exception("More than 1 full token match")

            elif len(res["true"]) == 1:
                if len(res["none"]) == 0:       #case - 1 full token match, no possible other matches
                    res_tokens.append(Token(res["true"][0], str_to_take, tuple(position)))
                    position[1] += len(str_to_take)
                    file_str = file_str[len(str_to_take):]
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
                        break

                    raise Exception("Unidentified token: ", str_to_take)

    return res_tokens