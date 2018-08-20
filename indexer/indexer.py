#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import nltk
import base64
import pickle
import logging
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from nltk.stem.snowball import SnowballStemmer

class Indexer:
    def __init__(self, verbose=False, path=None):
        self.logger = logging.getLogger("indexer")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("indexer.log")
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)
        self.verbose = verbose
        self.path = path

    def create_index(self):
        assert os.path.isdir(self.path), "Nonexistent document directory"
        os.system("rm -rf index; mkdir -p index")
        document_dir = os.fsencode(self.path)
        index = document_count = 0
        for i in os.listdir(document_dir):
            document_count += 1
        bar = IncrementalBar("Processing...", max = 21, suffix="%(percent)d%%")
        for document in os.listdir(document_dir):
            file_name = os.fsdecode(document)
            tokens = self.extract_tokens(os.path.join(self.path, file_name))
            if self.verbose:
                print("Indexing {}".format(base64.b16decode(document)))
                print(tokens)
            for (freq, tok) in tokens:
                file_name = os.path.join(b"index", base64.b16encode(tok.encode()))
                try:
                    f = open(file_name, "rb")
                    token = pickle.load(f)
                    f.close()
                except IOError:
                    token = []
                token.append((freq, document))
                try:
                    token_file = open(file_name, "wb")
                    pickle.dump(token, token_file)
                    token_file.close()
                except Exception as e:
                    self.logger.info("[create_index]: {}".format(e))
                    index -= 1
            if(index % int(document_count / 20) == 0):
                self.logger.info("[create_index]: %d/%d", index, document_count)
                bar.next()
            index += 1

    @staticmethod
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

    def extract_tokens(self, path):
        '''
        - Given the name of a document located in self.path, this method
        extracts its contents and returns a list of pairs
        [(x, y) | x = the frequency of the token, y = the token itself].
        '''
        stemmer = SnowballStemmer("english")
        words = list()
        terms = dict()
        with open(path) as f:
            soup = BeautifulSoup(f.read(), "lxml")
        data = soup.findAll(text=True)
        clean = [i.lower() for i in list(filter(Indexer.visible, data))]
        sw = nltk.corpus.stopwords.words("english")
        for i in clean:
            tok_freq = 0
            tokens = re.findall("\w+", i)
            for tok in tokens:
                if tok not in sw:
                    words.append(stemmer.stem(tok))
        for word in words:
            terms[word] = 1 if word not in terms else terms[word] + 1
        return set([(terms[i], i) for i in words])

    def __del__(self):
        self.logger.info("Object destroyed")
