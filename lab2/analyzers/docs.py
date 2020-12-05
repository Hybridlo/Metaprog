from util import *


def javadoc_to_slashes(verif_file, fix_file, filepath, file_data):
    i = 0
    in_javadoc = False
    new_data = ""
    changed = False

    while i < len(file_data):
        if file_data[i:i+3] == "/**":
            in_javadoc = True
            changed = True

        if in_javadoc:
            line = read_until_newline(file_data)
            i += len(line)
            line = remove_star_in_line(line)

            if line == None:
                in_javadoc = False
                continue

            new_data += "/// " + line

        new_data += file_data[i]
        i += 1

    if changed:
        verif_file.write(f"{filepath} Warning: Javadoc-style block comments not allowed")
        fix_file.write(f"{filepath} Changed: Javadoc-style block comments transformed into ///")

    return new_data
