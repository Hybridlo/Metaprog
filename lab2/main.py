import argparse
from pathlib import Path

#folder to store results
results_folder = Path("results/")

#specify file extention of interest
extention = "swift"

#create  and configure argparse
arg_parser = argparse.ArgumentParser(description="PHP formatter")

group1 = arg_parser.add_mutually_exclusive_group(required=True)
group1.add_argument("-d", action="store", dest="directory", help="directory to parse")
group1.add_argument("-f", action="store", dest="file", help="file to parse")
group1.add_argument("-p", action="store", dest="project", help="project directory to parse (recursive)")

arg_parser.add_argument("-v", "--verify", action="store_true", dest="verify", help="output errors.log")
arg_parser.add_argument("-fx", "--fix", action="store_true", dest="fix", help="create file/directory with formatted code following template in specified file")

args = arg_parser.parse_args()

def scan_and_fix_file(filepath, outname):
    with open(filepath, "r") as infile:
        data = infile.read()


if args.file:
    file = Path(args.file)

    outname = file.stem

    if not file.exists():
        raise FileNotFoundError("File not found")

    scan_and_fix_file(file, outname)

if args.directory:
    directory = Path(args.directory)

    outname = directory.stem

    if not directory.exists():
        raise FileNotFoundError("Directory not found")

    for filepath in directory.glob("*." + extention):
        scan_and_fix_file(filepath, outname)

if args.project:
    project = Path(args.project)

    outname = project.stem

    if not project.exists():
        raise FileNotFoundError("Project directory not found")

    for filepath in project.glob("**/*." + extention):
        scan_and_fix_file(filepath, outname)