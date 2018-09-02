#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from ranker import Ranker

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", default=None,\
                        help="Document path")
    parser.add_argument("-t", "--term", dest="term",\
                        help="The search term")
    args = parser.parse_args()
    assert args.term, "Please provide a search term"
    path = args.path
    term = args.term.encode()
    rank = Ranker(term) if path is None else Ranker(term, path)
    results = rank.get_results()
    if results:
        for (freq, link) in results:
            print("{} : {}".format(link, freq))
