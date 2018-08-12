#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import nltk
import base64
import pymysql
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from nltk.stem.snowball import SnowballStemmer

class Indexer:
    def __init__(self, path="documents", config="db-config.yml"):
        assert os.path.isdir(path), "Nonexistent document directory"
        assert os.path.exists(config), "Nonexistent configuration file"
        self.path = path
        self.config = config
        with open(self.config) as f:
            cfg = yaml.load(f)
        self.connection = pymysql.connect(host=cfg['host'],
                                     user=cfg['user'],
                                     charset="utf8",
                                     autocommit=True,
                                     use_unicode=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.connection.cursor().execute("CREATE SCHEMA IF NOT EXISTS `{}`;".format(cfg['db_name']))

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

    def map_documents(self):
        '''
        - This method defines a mapping between documents and document ids
        - It then saves this mapping into a mysql database whose configuration
        is to be specified in a yaml file passed through the constructor
        (see db-config.yml).
        '''
        self.connection.cursor().execute("DROP TABLE IF EXISTS `Search-Engine`.`doc_map`")
        self.connection.cursor().execute("CREATE TABLE `Search-Engine`.`doc_map` (\
        `ID` INT NOT NULL , `URL` VARCHAR(255) NOT NULL , PRIMARY KEY (`ID`))\
        ENGINE = InnoDB;")
        document_dir = os.fsencode(self.path)
        index = document_count = 0
        for i in os.listdir(document_dir):
            document_count += 1
        bar = IncrementalBar("Processing...", max = 21, suffix="%(percent)d%%")
        for document in os.listdir(document_dir):
            filename = os.fsdecode(document)
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `doc_map` (`ID`, `URL`) VALUES ('%s','%s');"
                cursor.execute(sql % (index, filename))
                if(index % int(document_count / 20) == 0):
                    bar.next()
                index += 1
        bar.finish()

    def map_tokens(self):
        '''
        - This method defines a mapping between tokens and token-ids.
        - It then saves this mapping into a mysql database whose configuration
        is to be specified in a yaml file passed through the constructor
        (see db-config.yml).
        '''
        self.connection.cursor().execute("DROP TABLE IF EXISTS `Search-Engine`.`tokens`")
        self.connection.cursor().execute("CREATE TABLE `Search-Engine`.`tokens` ( `TOK` \
        VARCHAR(100) NOT NULL , `DOCS` TEXT NOT NULL , PRIMARY KEY (`TOK`)) ENGINE = InnoDB;")
        self.connection.cursor().execute("USE `Search-Engine`;")
        document_dir = os.fsencode(self.path)
        for document in os.listdir(document_dir):
            document = document.decode()
            tokens = self.extract_tokens(document)
            for tok in tokens:
                # Add token to the database if it hasn't already sent there
                enc = base64.b16encode(tok.encode()).decode()
                with self.connection.cursor() as cursor:
                    if cursor.execute("SELECT * from `tokens` WHERE TOK='{}'".format(enc)):
                        docs = cursor.fetchone()['DOCS'].split(',')
                        docs.append(document)
                        update_str = ",".join(docs)
                        cursor.execute("UPDATE `tokens` SET `DOCS`='{}' WHERE 1;".format(update_str))
                    else:
                        sql = "INSERT INTO `tokens` (`TOK`, `DOCS`) VALUES ('%s', '%s')"
                        print(sql % (enc, document))
                        cursor.execute(sql % (enc, document))

    def extract_tokens(self, document, stemming=False):
        '''
        - Given the name of a document located in self.path, this method
        extracts its contents and returns the tokens it contains.
        - If stemming is true, only the stem of each token will be returned.
        '''
        stemmer = SnowballStemmer("english")
        words = list()
        terms = dict()
        with open(os.path.join(self.path, document)) as f:
            soup = BeautifulSoup(f.read(), "lxml")
        data = soup.findAll(text=True)
        clean = [i.lower() for i in list(filter(Indexer.visible, data))]
        sw = nltk.corpus.stopwords.words("english")
        for i in clean:
            tokens = re.findall("\w+", i)
            for tok in tokens:
                if tok not in sw:
                    if stemming:
                        words.append(stemmer.stem(tok))
                    else:
                        words.append(tok)
        for word in words:
            terms[word] = 1 if word not in terms else terms[word] + 1
        return words

    def __del__(self):
        self.connection.close()
