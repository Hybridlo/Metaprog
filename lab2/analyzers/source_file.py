from util import *


def check_filename(verif_file, fix_file, filepath, file_data, filename):
    """Check types in a file, if there's one
    check filename for convention compliance,
    also check for extentions"""
    types = []
    extentions = []

    for i in range(0, len(file_data)):
        # check for class keyword
        if check_word_with_space(file_data[i:], "class"):
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
