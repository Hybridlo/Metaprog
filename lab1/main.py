from token.tokenizer import tokenize
from formatting.formatters import all_formatters
from formatting.options import Options

import argparse
from pathlib import Path

#folder to store results
results_folder = Path("results/")

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

def apply_min(adjustments, tokens, i):
    """if user didn't put enough newlines, add as much as needed"""
    if len(tokens) == i + 1:
        return

    user_newlines = tokens[i+1].pos_in_code[0] - tokens[i].pos_in_code[0]
    
    adjustments["newlines_after"] = max(adjustments["min_newlines"]+1, user_newlines)

    if tokens[i].in_code.endswith("\n"):        #account for newlines in single line comments
        adjustments["newlines_after"] -= 1

def apply_max(adjustments, tokens, i):
    """if user put too many newlines, remove as much as needed"""
    if len(tokens) == i + 1:
        return

    user_newlines = tokens[i+1].pos_in_code[0] - tokens[i].pos_in_code[0]
    
    adjustments["newlines_after"] = min(adjustments["max_newlines"]+1, user_newlines)

    if tokens[i].in_code.endswith("\n"):        #account for newlines in single line comments
        adjustments["newlines_after"] -= 1

def format_file(outfile, tokens):
    curr_position = [1, 1]

    for i in range(len(tokens)):
        adjustments = {"spaces_before": 0, "spaces_after": 0, "newlines_before": 0, "newlines_after": 0,
                        "min_newlines": 0, "max_newlines": 0}

        tokens[i].position = tuple(curr_position)      #to track newlines properly

        do_apply_min = False
        do_apply_max = False

        for formatter in all_formatters:
            tmp_adj = formatter(tokens, i, config)

            for key in tmp_adj:
                if key == "min_newlines" and tmp_adj[key] > -1:     #to not add -1, -1 indicates not to format
                    adjustments[key] = max(tmp_adj[key], adjustments[key])
                    do_apply_min = True

                elif key == "max_newlines" and tmp_adj[key] > -1:
                    adjustments[key] = max(tmp_adj[key], adjustments[key])
                    do_apply_max = True
                
                elif key in ["spaces_before", "spaces_after", "newlines_before", "newlines_after"]:
                    adjustments[key] += tmp_adj[key]

        if do_apply_max:
            apply_max(adjustments, tokens, i)

        if do_apply_min:
            apply_min(adjustments, tokens, i)

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

#apply -v and -f to tokenized file
def finish_file(filepath, errors_file, tokens, errors):

    #print errors to errors.log
    if args.verify:
        results_folder.mkdir(exist_ok=True)
        
        for error in errors:
            errors_file.write(str(filepath) + ": " + error + "\n")
    
    if len(errors) == 0:
        if args.template:
            with open(filepath, "w+") as outfile:
                format_file(outfile, tokens)
                
    else:
        print(f"Errors found in {filepath}, use -v and check results/errors.log")

def scan_file(filepath, errors_file):
    with open(filepath, "r") as infile:
        data = infile.read()

        tokens, errors = tokenize(data)

        finish_file(filepath, errors_file, tokens, errors)

if args.file:
    outfile = open(results_folder / "errors.log", "a+")
    scan_file(args.file, outfile)

if args.directory:
    directory = Path(args.directory)
    outfile = open(results_folder / "errors.log", "a+")

    if not directory.exists():
        raise FileNotFoundError("Directory not found")

    for filepath in directory.glob("*." + extention):
        scan_file(filepath, outfile)

if args.project:
    project = Path(args.project)
    outfile = open(results_folder / "errors.log", "a+")

    if not project.exists():
        raise FileNotFoundError("Project directory not found")

    for filepath in project.glob("**/*." + extention):
        scan_file(filepath, outfile)