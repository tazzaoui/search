#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains the logic used to tokenize html files.
"""

import re
from bs4 import BeautifulSoup
import nltk
from nltk.stem.snowball import SnowballStemmer


def exclusion_policy(element):
    '''
    Defines the exclusion policy for html text extraction
    '''
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    elif element.isspace():
        return False
    return True


def extract_tokens(path):
    '''
    - Given the path to a document, this method
    extracts its contents and returns a list of pairs
    [(x, y) | x = the frequency of the token, y = the token itself].
    '''
    stemmer = SnowballStemmer("english")
    words = list()
    terms = dict()
    with open(path) as document:
        soup = BeautifulSoup(document.read(), "lxml")
    data = soup.findAll(text=True)
    clean = [i.lower() for i in list(filter(exclusion_policy, data))]
    stop_words = nltk.corpus.stopwords.words("english")
    for i in clean:
        tokens = re.findall(r"\w+", i)
        for tok in tokens:
            if tok not in stop_words:
                words.append(stemmer.stem(tok))
    for word in words:
        terms[word] = 1 if word not in terms else terms[word] + 1
    return set([(terms[i], i) for i in words])
