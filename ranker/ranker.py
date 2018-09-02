#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import pickle

class Ranker:
    def __init__(self, search_term, docs_path=b"test-docs"):
        self.tf = 0
        self.idf = 0
        self.term = search_term
        self.docs_path = docs_path

        search_results = self.search()
        if search_results is None:
            self.search_results = None
        else:
            self.search_results = [(x, base64.b16decode(y)) for (x, y) in search_results]

    def search(self):
        """
        Search if a term exists, if so, return a list of tuples
        (x, y) s.t. x = a document & y = the term's document frequency
        """
        encoded_term = base64.b16encode(self.term)
        index_path = os.path.abspath(self.docs_path)
        term_file = os.path.join(index_path, encoded_term.decode())
        if not os.path.exists(term_file):
            print("The term '{}' was not found".format(self.term.decode()))
            return None
        with open(term_file, "rb") as index_file:
            return pickle.load(index_file)

    def get_results(self):
        return self.search_results
