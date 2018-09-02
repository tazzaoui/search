#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the vector operations
used for modeling the corpus and ranking documents.
"""

import os
import math
from support.token import extract_tokens

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
        assert os.path.exists(doc_path), "No such path {}:".format(doc_path)
        counts = dict()
        tokens = extract_tokens(os.path.abspath(doc_path))
        for token in tokens:
            counts[token] = counts[token] + 1 if token in counts else 1
        self.values = counts.values()

    def __mul__(self, other):
        """
        @param other: Multiplication is defined for
                        * A vector: in which case, the dot product of the two vectors
                        is returned.
                        * A scalar: in which case, each element of the vector will be
                        multiplied by the constant.
        """
        if isinstance(other, (int, float)):
            return [val * other for val in self.values]
        if isinstance(other, Vector):
            assert len(other.values) == len(self.values)
            result = 0
            for element in range(len(self.values)):
                result += self.values[element] * other.values[element]
            return result
        raise ValueError("Vector multiplication is only defined for scalars or other vectors")

    def euclidean_norm(self):
        """
        @param vector: An n-dimensional vector (list of numbers)
        @return float: The euclidean norm of the vector
        """
        sum_of_squares = 0
        for element in self.values:
            sum_of_squares += element**2
        return math.sqrt(sum_of_squares)

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
