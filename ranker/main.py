#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser
from ranker import Ranker

def main():
    default_docs_path = os.path.abspath("../../test-index")
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", default=None,\
                        help="Document path")
    parser.add_argument("-t", "--term", dest="term",\
                        help="the search term")
    args = parser.parse_args()
    assert args.term, "Please provide a search term!"
    path = args.path.encode() if args.path else default_docs_path
    term = args.term.encode()
    rank = Ranker(term, path)
    results = rank.get_results()
    if results:
        for (freq, link) in results:
            print("{} : {}".format(link, freq))
        return

if __name__ == "__main__":
    main()
