SEPARATORS = [" ", "\n", "{", "}", "=", ">", "<", ":", "?", ",", "\"", "\'"]


def get_next_word_indices(data):
    """Get indices between separators,
    skipping separators at start"""

    start = None

    for i in range(0, len(data)):
        if start == None and data[i] not in SEPARATORS:
            start = i

        if start != None and data[i] in SEPARATORS:
            return start, i

    return None  # file read until EOF


def read_next_word(data):
    """Read the word, disregard indices"""
    start, end = get_next_word_indices(data)

    return data[start:end]


def check_word_with_space(data, word):
    """Checks for a type"""

    word_len = len(word)

    if len(data) < word_len + 1:
        return False

    if data[:word_len+1] == word + " ":
        return True

    return False
