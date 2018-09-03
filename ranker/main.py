#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser
from ranker.term import Term
from ranker.vector import Vector

def main(term, index_path):
    term = Term(term)
    search_results = term.get_search_results()
    query = Vector(index_path, "query")
    similarity = dict()
    if search_results is None:
        print("No Results!")
        return False
    else:
        for document in search_results:
            vec = Vector(index_path, document)
            similarity[document] = query.cosine_similarity(vec)

    print(similarity)

if __name__ == "__main__":
    default_docs_path = os.path.abspath("../../test-index")
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", default=None,\
                        help="Document path")
    parser.add_argument("-t", "--term", dest="term",\
                        help="the search term")
    args = parser.parse_args()
    assert args.term, "Please provide a search term!"
    path = args.path if args.path else default_docs_path
    term = args.term.encode()
    main(term, path)
