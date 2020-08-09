from argparse import ArgumentParser

from . import yield_to_csv, analyze_history

parser = ArgumentParser(description="Get line counts and complexity measurements from a Python package's git repo's history.")
parser.add_argument("project_path", help="The path to the folder you want to analyze")
parser.add_argument("output_csv", help="The csv file path you want to create.")

args = parser.parse_args()

yield_to_csv(analyze_history(repo=args.project_path), args.output_csv)