#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import nltk
import sys
import pymongo
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from argparse import ArgumentParser

def visible(element):
    '''
        - Defines the exclusion policy for html text extraction
    '''
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    elif element.isspace():
        return False
    return True

def extract_words(document):
    words = set()
    soup = BeautifulSoup(document, "lxml")
    data = soup.findAll(text=True)
    clean = [i.lower() for i in list(filter(visible, data))]
    sw = nltk.corpus.stopwords.words('english')
    for i in clean:
        tokens = re.findall('\w+', i)
        for tok in tokens:
            if tok not in sw:
                words.add(tok)
    return words

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        words = extract_words(f.read())
    print(words)
