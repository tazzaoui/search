#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the vector operations
used for modeling the corpus and ranking documents.
"""

import os
import base64
import pickle
import numpy as np
from ranker.term import Term
from support.token_extract import extract_tokens

class Vector:
    """
    This class implementats the vector operations
    used for modeling the corpus and ranking documents.
    """
    def __init__(self, doc_path):
        """
        @param doc_path: The path to a file representing
                         a document in the corpus
        """
        doc_path = os.path.abspath(doc_path)
        assert os.path.exists(doc_path), "No such path: {}".format(doc_path)
        num_docs = len(os.listdir(os.path.join(doc_path, "..")))

        if not os.path.exists("unique_terms.pickle"):
            unique_terms = set()
            for term_file in os.listdir(doc_path):
                unique_terms.add(base64.b16decode(term_file))
            with open("unique_terms.pickle", "wb") as output_file:
                pickle.dump(list(unique_terms), output_file)
        else:
            with open("unique_terms.pickle", "rb") as input_file:
                unique_terms = pickle.load(input_file)

        tokens = extract_tokens(doc_path)
        values = list()
        for term in unique_terms:
            if term in tokens:
                term_obj = Term(term)
                doc_freq = term_obj.get_document_frequency()
                inv_document_freq = np.log(num_docs/doc_freq)
                doc_id = doc_path.split("/")[-1].strip()
                term_frequency = term.get_term_frequency()[doc_id]
                values.append(term_frequency * inv_document_freq)
            else:
                values.append(0)
        self.__values = np.array(values)

    def euclidean_norm(self):
        """
        @param vector: An n-dimensional vector (list of numbers)
        @return float: The euclidean norm of the vector
        """
        return np.linalg.norm(self.__values)

    def cosine_similarity(self, vector):
        """
        @param vector: An n-dimensional vector (list of numbers)
        @return float: The cosine similarity between the two vectors
                       similarity = cos(x) = (A*B)/(|A|*|B|) defined
                       according to the definition of the dot product.
        """
        dot_prod = self.__mul__(vector)
        norm_a = self.euclidean_norm()
        norm_b = vector.euclidean_norm()
        assert norm_a != 0 and norm_b != 0
        return dot_prod / (norm_a * norm_b)

    def get_values(self):
        """
        @return numpy.array: An n-dimensional vector representation of the
                             document
        """
        return self.__values

    def __mul__(self, other):
        """
        @param other: Multiplication is defined for
                        * A vector: in which case, the dot product of the two vectors
                        is returned.
                        * A scalar: in which case, each element of the vector will be
                        multiplied by the constant.
        """
        if isinstance(other, (int, float)):
            return other * self.__values
        if isinstance(other, Vector):
            assert len(self.__values) == len(other.get_values())
            return np.dot(self.__values(), other.get_values())
        raise ValueError("Vector multiplication is defined only for scalars or other vectors")
