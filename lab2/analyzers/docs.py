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
            line = read_until_newline(file_data[i:])
            i += len(line)
            line = remove_star_in_line(line)

            if line == None:
                in_javadoc = False
                continue

            new_data += "/// " + line

        new_data += file_data[i]
        i += 1

    if changed:
        verif_file.write(
            f"{filepath} Warning: Javadoc-style block comments not allowed")
        fix_file.write(
            f"{filepath} Changed: Javadoc-style block comments transformed into ///")

    return new_data


def comment_tags(verif_file, fix_file, filepath, file_data):
    i = 0
    new_file_data = ""
    warnings = []
    changes = []

    while i < len(file_data):
        if file_data[i:i+3] == "///":
            comment_lines, flags, count, i = process_doc_block(file_data[i:])

            if not check_tags_order(flags):
                verif_file.write(
                    f"{filepath} Error: tags in doc block are in the wrong order")

            new_block_lines, changes, warnings = redo_comment_block(
                comment_lines, count, filepath)

            new_block = "\n".join(new_block_lines)
            i += len(new_block)
            new_file_data += new_block

        new_file_data += file_data[i]
        i += 1

    for warning in warnings:
        verif_file.write(warning)

    for change in changes:
        fix_file.write(change)

    return new_file_data
