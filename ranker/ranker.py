#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import base64
import pickle
from support.vector import vectorize_document
from support.vector import euclidean_norm

class Ranker:
    def __init__(self, search_term, index_path):
        total_docs = 100
        self.term = search_term
        self.index_path = index_path
        search_results = self.search()
        self.search_results = [(x, base64.b16decode(y)) for (x, y) \
                              in search_results] if search_results else None
        self.tf = [freq for (freq, url) in self.search_results]
        # Create the document vector
        i = 0
        for doc in self.search_results:
            document_vector = vectorize_document(doc)
            self.tf[i] /= euclidean_norm(document_vector)
        self.idf = math.log(total_docs / len(self.search_results))

    def search(self):
        """
        Search if a term exists, if so, return a list of tuples
        (x, y) s.t. x = a document & y = the term's document frequency
        """
        encoded_term = base64.b16encode(self.term)
        index_path = os.path.abspath(self.index_path)
        term_file = os.path.join(index_path, encoded_term.decode())
        if not os.path.exists(term_file):
            print("The term '{}' was not found".format(self.term.decode()))
            return None
        with open(term_file, "rb") as index_file:
            return pickle.load(index_file)

    def list_terms(self):
        """
        @return list: A list of tupples representing the terms available in the index.
        """
        terms = []
        for term in os.listdir(self.index_path):
            terms.append(base64.b16decode(term).decode())
        return terms

    def get_results(self):
        """
        @return list:  A list of tupples representing the term's search results
        """
        return self.search_results
