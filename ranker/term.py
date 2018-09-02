#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import pickle


class Term:
    """
    This class provides a high-level API for interacting with search terms.
    It provides the ability to search for a term in the corpus. If the term
    exists it makes available the list of documents the term can be found in
    as wel the term's frequency within each document.
    """

    def __init__(self, search_term, index_path):
        self.__term = str(search_term)
        self.__index_path = index_path
        self.__exists = bool(self.search is not None)
        self.__term_frequencies = [freq for (freq, url) in self.search()]
        self.__search_results = [url for (freq, url) in self.search()]

    def search(self):
        """
        Search if a term exists, if so, return a list of tuples
        (x, y) s.t. x = a document & y = the term's document frequency
        """
        encoded_term = base64.b16encode(self.__term)
        index_path = os.path.abspath(self.__index_path)
        term_file = os.path.join(index_path, encoded_term.decode())
        if not os.path.exists(term_file):
            return None
        with open(term_file, "rb") as index_file:
            return pickle.load(index_file)

    def list_terms(self):
        """
        @return list: A list of tupples representing the terms available in the index.
        """
        terms = []
        for term in os.listdir(self.__index_path):
            terms.append(base64.b16decode(term).decode())
        return terms

    def get_search_results(self):
        """
        @return list:  A list of strings representing the document-id of every
        document that contains the term
        """
        return self.__search_results

    def get_term_frequencies(self):
        """
        @return list:  A list of integers represting the term's frequency in
                       document i
        """
        return self.__term_frequencies

    def exists(self):
        """
        @return Bool:  True if the term exists in the corpus, false otherwise
        """
        return self.exists

    def __str__(self):
        return self.__term
