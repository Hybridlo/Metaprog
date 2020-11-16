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

#apply -v and -f to tokenized file
def finish_file(project_dir, file_path, infile, tokens, errors):
    #print errors to errors.log
    if args.verify:
        os.makedirs(results_folder + project_dir, exist_ok=True)
        with open(results_folder + project_dir + "\\errors.log", "a+") as outfile:
            for error in errors:
                outfile.write(infile.name + ": " + error + "\n")

    #TODO: create formatted file(s)
    if len(errors) == 0:
        config = Options("default")
        curr_position = [1, 1]

        for i in range(len(tokens)):
            adjustments = {"spaces_before": 0, "spaces_after": 0, "newlines_before": 0, "newlines_after": 0}
            tokens[i].curr_position = tuple(curr_position)      #to track newlines properly

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

            tokens[i].curr_position = tuple(curr_position)      #to track newlines properly

            if adjustments["newlines_after"] == 0:
                res_str = res_str + " " * adjustments["spaces_after"]
                curr_position[1] += adjustments["spaces_after"]
            else:
                curr_position[0] += adjustments["newlines_after"]
                curr_position[1] = 1

            print(res_str, end="")

def scan_file(filename, project_dir="", file_path=""):
    if file_path != "":
        file_path += "\\"

    with open(file_path + filename, "r") as infile:
        data = infile.read()

        tokens, errors = tokenize(data)

        if project_dir == "":
            finish_file(infile.name, "", infile, tokens, errors)
        else:
            finish_file(project_dir, file_path, infile, tokens, errors)

if args.file:
    scan_file(args.file)

if args.directory:
    for item in os.listdir(args.directory):
        if item[-(1 + len(extention)):] == "." + extention:   #only check files with specified extention
            scan_file(item, args.directory, args.directory)

if args.project:
    for path, dirs, files in os.walk(args.project):
        for filename in files:
            scan_file(filename, args.project, path)