from util import *


def check_initializers(verif_file, fix_file, filepath, file_data):
    i = 0

    while i < len(file_data):
        word, i = read_next_word_and_end(file_data[i:])

        if word == "init":
            symbols_in_parentheses, i = get_symbols_in_parentheses(file_data)
            vars_directly_assigned = get_vars_directly_assigned(
                file_data, symbols_in_parentheses)
            new_data, changes = apply_init_changes(
                file_data, symbols_in_parentheses, vars_directly_assigned, filepath)

            if len(changes) > 0:
                verif_file.write(
                    f"{filepath} Error: init parameters direct assignment should have same name as field")

                for change in changes:
                    fix_file.write(change)

            return new_data
