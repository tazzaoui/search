#!/usr/bin/env python

"""
This file is for converting a set of articles to a set of tokens.
"""
import os
import base64
from support.token_extract import extract_tokens

input_files = os.path.abspath("../indexer/raw")
output_dir = os.path.abspath("../indexer/tokenized-raw")
os.system("rm -rf ../indexer/tokenized-raw; mkdir ../indexer/tokenized-raw")

for input_file in os.listdir(input_files):
    tokens = [y for (x,y) in extract_tokens(os.path.join(input_files, input_file))]
    encoded_file_name = base64.b16encode(input_file.encode())
    with open(os.path.join(output_dir, input_file), "w") as f:
        with open(os.path.join(input_files, input_file), "r") as f1:
            f.write(f1.readline())
        f.write("\n".join(tokens))
