from .parser import JsonExplorer
import argparse
import json
import logging

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('key', type=str, help='Key to parse')
    parser.add_argument('-v', '--verbose', help='Verbose', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--input', type=str, help='Raw JSON data')
    group.add_argument('--input-file', type=str, help='Path to JSON File')
    return parser.parse_args()

def clean_print_from_result(result):
    if(len(result) == 0):
        print("0 result")

    max_col = [0 for col in result[0]]
    for row in result:
        for id_col, col in enumerate(row):
            if(len(str(col)) > max_col[id_col]):
                max_col[id_col] = len(str(col))

    for row in result:
        print("".join(str(word).ljust(max_col[id_word] + 2) for id_word, word in enumerate(row)))

def main():
    args = parse_args()
    input_raw = ""
    if(args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    if(args.input_file):
        with open(args.input_file, mode="r") as f:
            input_raw = f.read()
    else:
        input_raw = args.input
    json_data = json.loads(input_raw)
    obj = JsonExplorer()
    obj.parse_and_explore(args.key, json_data)
    clean_print_from_result(obj.flatten_results())


