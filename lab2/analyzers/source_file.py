from util import *
import re


def check_filename(verif_file, fix_file, filepath, file_data, filename):
    """Check types in a file, if there's one
    check filename for convention compliance,
    also check for extentions"""
    types = []
    extentions = []

    for i in range(0, len(file_data)):
        # check for class keyword
        if check_word_with_space(file_data[i:], "class") and not check_word_with_space(file_data[i:], "class var"):
            types.append(read_next_word(file_data[i+6:]))

        # check struct keyword
        if check_word_with_space(file_data[i:], "struct"):
            types.append(read_next_word(file_data[i+6:]))

        # check type extention
        if check_word_with_space(file_data[i:], "extention"):
            # get type being extended
            offset = len("extention ")
            start, end = get_next_word_indices(file_data[i+offset:])
            decl_type = file_data[start:end]
            types.append(decl_type)

            # get first extention
            offset = end
            start, end = get_next_word_indices(file_data[i+offset:])
            extention1 = file_data[start:end]
            extentions.append(extention1)

            # perform check for second extention (by searching for comma)
            second_extention = False

            for j in range(end, len(file_data)):
                if file_data[j] == " ":
                    continue

                elif file_data[j] == ",":
                    second_extention = True

                break

            # get second extention if it exists, no need to check for more
            if second_extention:
                offset = end
                start, end = get_next_word_indices(file_data[i+offset:])
                extention2 = file_data[start:end]
                extentions.append(extention2)

    if len(types) == 1:
        if len(extentions) == 0:
            if filename != types[0]:
                verif_file.write(
                    f"{filepath} Error: file name with one type must match type it's declaring")

        elif len(extentions) == 1:
            if filename != types[0] + "+" + extentions[0]:
                verif_file.write(
                    f"{filepath} Error: file name with one type single extention must match TypeName+Protocol")

        else:
            if not filename.startswith(types[0] + "+"):
                verif_file.write(
                    f"{filepath} Error: file name with one type multiple extentions must match TypeName+Stuff")


def various_char_checks(verif_file, fix_file, filepath, file_data, filename):
    """Checks source file for not allowed spaces

    Checks for unicode escaped characters that
    can be written as special escape sequence"""

    for i in range(0, len(file_data)):
        if (re.match(r"\s", file_data[i]) and file_data[i] != " "
                and file_data[i] != "\n" and file_data[i:i+2] != "\r\n"):

            verif_file.write(
                f"{filepath} Error: source file contains illegal whitespace characters")

        if (file_data[i:i+5] in [r"\u{0}", r"\u{9}", r"\u{A}", r"\u{D}"]
                or file_data[i:i+6] in [r"\u{22}", r"\u{27}", r"\u{5C}"]):

            verif_file.write(
                f"{filepath} Error: source file contains unicode escaped chars that can be represented as special escaped char")
