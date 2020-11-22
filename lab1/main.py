from token.tokenizer import tokenize
from formatting.formatters import all_formatters
from formatting.options import Options

import argparse
import os

#folder to store results
results_folder = "results/"

#specify file extention of interest
extention = "php"

#create  and configure argparse
arg_parser = argparse.ArgumentParser(description="PHP formatter")

group1 = arg_parser.add_mutually_exclusive_group(required=True)
group1.add_argument("-d", action="store", dest="directory", help="directory to parse")
group1.add_argument("-f", action="store", dest="file", help="file to parse")
group1.add_argument("-p", action="store", dest="project", help="project directory to parse (recursive)")

arg_parser.add_argument("-v", "--verify", action="store_true", dest="verify", help="output errors.log")
arg_parser.add_argument("-fr", "--format", action="store", dest="template", help="create file/directory with formatted code following template in specified file")

args = arg_parser.parse_args()

if args.template:
    config = Options(args.template)

#apply -v and -f to tokenized file
def finish_file(proj_path, proj_name, infile, tokens, errors):
    file_in_proj_path = os.path.relpath(proj_path, os.path.dirname(infile.name))
    file_path = proj_name + file_in_proj_path
    filename = os.path.basename(infile.name)

    if proj_name == "":
        proj_name = filename

    #print errors to errors.log
    if args.verify:
        os.makedirs(results_folder + proj_name, exist_ok=True)
        with open(results_folder + proj_name + "\\errors.log", "a+") as outfile:
            for error in errors:
                outfile.write(infile.name + ": " + error + "\n")
    
    if len(errors) == 0:
        curr_position = [1, 1]

        if args.template:
            os.makedirs(results_folder + file_path, exist_ok=True)
            with open(results_folder + file_path + "\\" + filename, "w+") as outfile:
                for i in range(len(tokens)):
                    adjustments = {"spaces_before": 0, "spaces_after": 0, "newlines_before": 0, "newlines_after": 0}
                    tokens[i].position = tuple(curr_position)      #to track newlines properly

                    for formatter in all_formatters:
                        tmp_adj = formatter(tokens, i, config)

                        for key in tmp_adj:
                            adjustments[key] += tmp_adj[key]

                    res_str = tokens[i].in_code
                    res_str = "\n" * adjustments["newlines_before"] + res_str
                    res_str = res_str + "\n" * adjustments["newlines_after"]

                    if adjustments["newlines_before"] == 0:
                        res_str = " " * adjustments["spaces_before"] + res_str
                        curr_position[1] += adjustments["spaces_before"]
                    else:
                        curr_position[0] += adjustments["newlines_before"]
                        curr_position[1] = 1

                    tokens[i].position = tuple(curr_position)      #to track newlines properly

                    if adjustments["newlines_after"] == 0:
                        res_str = res_str + " " * adjustments["spaces_after"]
                        curr_position[1] += adjustments["spaces_after"]
                    else:
                        curr_position[0] += adjustments["newlines_after"]
                        curr_position[1] = 1

                    for letter in tokens[i].in_code:
                        if letter == "\n":
                            curr_position[0] += 1

                    outfile.write(res_str)
                    outfile.flush()
    
    else:
        print(f"Errors found in {filename}, use -v and check errors.log")

def scan_file(filename, proj_name="", file_path=""):
    if file_path != "":
        file_path += "\\"

    with open(file_path + filename, "r") as infile:
        data = infile.read()

        tokens, errors = tokenize(data)

        if file_path == "":
            finish_file(infile.name, "", infile, tokens, errors)
        else:
            finish_file(file_path, proj_name, infile, tokens, errors)

if args.file:
    scan_file(args.file)

if args.directory:
    if args.directory[-1] != "/":
        args.directory += "/"

    for item in os.listdir(args.directory):
        if item[-(1 + len(extention)):] == "." + extention:   #only check files with specified extention
            proj_name = os.path.basename(os.path.dirname(args.directory))
            print(proj_name)
            scan_file(item, proj_name, args.directory)

if args.project:
    if args.project[-1] != "/":
        args.project += "/"

    for path, dirs, files in os.walk(args.project):
        for filename in files:
            proj_name = os.path.basename(os.path.dirname(args.project))
            scan_file(filename, proj_name, path)