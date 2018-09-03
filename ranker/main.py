#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from argparse import ArgumentParser
from ranker.term import Term
from ranker.vector import Vector
from support.token_extract import extract_tokens


def main(index_path, search_term):
    with open("../indexer/index/query", "w") as query_file:
        query_file.write("{}\n".format(search_term))
    query_tokens = extract_tokens(os.path.join(index_path, "query"))
    query = Vector("query")
    similarity = dict()
    t = Term(search_term.encode())
    search_results = t.search()
    if search_results is None:
        return list()
    else:
        for document in [y for (x, y) in search_results]:
            vec = Vector(document.decode())
            similarity[document] = query.cosine_similarity(vec)
    return sorted(similarity.items(), key=lambda x: x[1], reverse=True)


def file_to_link(path):
    """
    Given a raw Wikipedia article, this method extracts its title,
    and returns a link to its page
    """
    with open(os.path.abspath(path), "r") as article:
        header = article.readline()
    title = header[7:]
    return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")


if __name__ == "__main__":
    default_docs_path = os.path.abspath("../../test-index")
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", default=None,
                        help="Document path")
    parser.add_argument("-t", "--term", dest="term",
                        help="the search term")
    args = parser.parse_args()
    path = args.path if args.path else default_docs_path
    search_term = input("Please enter your query: ")
    print("Searching...\n")
    initial_time = time.time()
    results = main(path, search_term)
    for path, sim in results:
        print(
            "[{}]\t{}".format(
                sim,
                file_to_link(
                    os.path.join(
                        b"../indexer/raw",
                        path))))
    print("Found {} results in {} seconds.".format(
        len(results), time.time() - initial_time))
