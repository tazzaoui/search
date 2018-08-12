#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from argparse import ArgumentParser
from indexer import Indexer

def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", \
                        help="Path of configuration file")
    parser.add_argument("-p", "--path", dest="path", \
                        help="Path of configuration file")
    parser.add_argument("-d", "--documents", dest="docs",\
                        help="Map documents to doc-ids")
    parser.add_argument("-w", "--words", dest="words",\
                        action="store_true",\
                        help="Extract words from docs")

    args = parser.parse_args()
    config = args.config if args.config else "db-config.yml"
    path = args.path if args.path else "test-docs"
    documents = True if args.docs else False
    words = True if args.words else False

    indexer = Indexer(path, config)
    if documents:
        indexer.map_documents()
    if words:
        indexer.map_tokens()

if __name__ == "__main__":
    main()
