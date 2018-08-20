#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os
import sys
from argparse import ArgumentParser
from indexer import Indexer

def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", default=None,\
                        help="Document path")
    parser.add_argument("-e", "--extract", dest="extract",\
                        help="Path to an html file from which to extract tokens")
    parser.add_argument("-v", dest="verbose", action="store_true",\
                        help="Verbose output")
    args = parser.parse_args()
    path = args.path
    verbose = True if args.verbose else False
    indexer = Indexer(verbose, path)
    if args.extract:
        string = indexer.extract_tokens(args.extract)
        with open("output.txt", "w") as w:
            w.write("{}".format(string))
        print(string)
    else:
        indexer.create_index()

if __name__ == "__main__":
    main()
