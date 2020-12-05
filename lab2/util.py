SEPARATORS = [" ", "\n", "\r", "{", "}", "=", ">",
              "<", ":", "?", ",", "\"", "\'", "(", ")"]


def next_separator_without_spaces_index(data):
    """Get index of next separator
    that is not a space"""

    tmp_seps = SEPARATORS[:]
    tmp_seps.remove(" ")
    tmp_seps.remove("\n")
    tmp_seps.remove("\r")

    for i in range(0, len(data)):
        if data[i] in tmp_seps:
            return i

        elif data[i] in [" ", "\n", "\r"]:
            continue

        break

    return None  # EOF or non-separator


def get_next_separator_without_spaces(data):
    """Get next separator that is not a space"""

    index = next_separator_without_spaces_index(data)

    return data[index]


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


def read_next_word_and_end(data):
    """Read the word, give end index"""
    start, end = get_next_word_indices(data)

    return data[start:end], end


def check_word_with_space(data, word):
    """Checks for a type"""

    word_len = len(word)

    if len(data) < word_len + 1:
        return False

    if data[:word_len+1] == word + " ":
        return True

    return False


def get_symbols_in_parentheses(data):
    """Get parameter names in parentheses"""

    if get_next_separator_without_spaces(data) != "(":
        return None

    i = 0
    res = {}

    while get_next_separator_without_spaces(data[i:]) != ")":
        word1, i = read_next_word_and_end(data[i:])
        word2 = None

        if get_next_separator_without_spaces(data[i]) == None:
            word2, i = read_next_word_and_end(data[i:])

        # res[outerName] = innerName
        if word2 != None:
            res[word1] = word2
        else:
            res[word1] = word1

        # disregard parameter type
        _, i = read_next_word_and_end(data[i:])

    return res, i


def is_next_newline(data):
    for i in range(len(data)):
        if data[i] == "\n":
            return True

        elif data[i] in [" ", "\r"]:
            continue

        return False


def get_vars_directly_assigned(data, symbols):
    res = {}
    newline = False
    i = 0
    nesting = 0

    while i < len(data):
        if data[i] == "\n":
            newline = True
            continue

        if data[i] == "{":
            nesting += 1

        if data[i] == "}":
            nesting -= 1

            if nesting == 0:
                break

        if newline == True:
            word1, i = read_next_word_and_end(data[i:])

            if get_next_separator_without_spaces(data[i:]) == "=":
                word2, i = read_next_word_and_end(data[i:])

                if is_next_newline(data[i:]) and word2 in symbols.values() and not word1.startswith("self."):
                    res[word1] = word2  # word1 = word2

        i += 1

    return res


def apply_init_changes(file_data, symbols_in_parentheses, vars_directly_assigned, filepath):
    i = 0
    start = None
    changes = []

    while i < len(file_data):
        word, i = read_next_word_and_end(file_data[i:])

        if word == "init":
            start = i

    if start == None:
        return None

    unprocessed = file_data[start:]

    new_file_data = file_data[:start]

    # modify parameters to match type fields
    for key in symbols_in_parentheses.keys():
        if symbols_in_parentheses[key] in vars_directly_assigned.values():
            start_change = unprocessed.index(key)
            new_file_data += unprocessed[:start_change]
            unprocessed = unprocessed[start_change:]

            word1, i = read_next_word_and_end(unprocessed)
            word2, i = read_next_word_and_end(i)

            unprocessed = unprocessed[i:]

            for k, v in vars_directly_assigned.items():
                if symbols_in_parentheses[key] == v:
                    new_file_data += k
                    break

    init_start = unprocessed.index("{")
    new_file_data += unprocessed[:init_start]
    unprocessed = unprocessed[init_start:]

    for key in vars_directly_assigned.keys():
        start_change = unprocessed.index(key)

        new_file_data += unprocessed[:start_change]
        unprocessed = unprocessed[start_change:]

        word1, i = read_next_word_and_end(unprocessed)
        word2, i = read_next_word_and_end(i)

        unprocessed = unprocessed[i:]

        new_file_data += f"self.{key} = {key}"

        changes.append(
            f"{filepath} Changed: parameter in init was changed to class field {key}")

    new_file_data += unprocessed

    return new_file_data, changes


def apply_static_class_prop_changes(data, all_changes, filepath):
    nesting = 0
    new_file_data = ""
    changes = []
    prop_changes = None

    while len(data) > 0:
        for class_change in all_changes.keys():
            if data[:len(class_change) + 6] == "class " + class_change:
                prop_changes = {}

        if prop_changes != None:
            if data[0] == "{":
                nesting += 1

            if data[0] == "}":
                nesting -= 1

                if nesting == 0:
                    prop_changes = None

            for change_prop in prop_changes.keys():
                if data[:len(change_prop)] == change_prop:
                    new_file_data += prop_changes[change_prop]
                    data = data[len(change_prop):]
                    changes.append(
                        f"{filepath} Changed: class/static property {change_prop} (doesn't need return suffix)")
                    break

            else:
                new_file_data += data[:1]
                data = data[1:]

    return new_file_data, changes
