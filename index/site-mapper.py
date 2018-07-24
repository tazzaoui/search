#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
- This script defines a mapping between documents and document ids
- It then saves this mapping into a non-relational database (mongodb)
'''

import os
import pymongo
import time
import sys
from progress.bar import IncrementalBar
from argparse import ArgumentParser

def map_sites(path):
    client = pymongo.MongoClient()
    db = client.search_engine
    db.doc_ids.drop()
    db.create_collection("doc_ids",
                         storageEngine={'wiredTiger':{'configString':'block_compressor=zlib'}})
    document_dir = os.fsencode(path)
    index = document_count = 0
    for i in os.listdir(document_dir):
        document_count += 1
    bar = IncrementalBar('Processing...', max=21, suffix="%(percent)d%%")
    for document in os.listdir(document_dir):
        filename = os.fsdecode(document)
        doc = {"_id": index, "URL": filename}
        db.doc_ids.insert_one(doc)
        if(index % int(document_count / 20) == 0):
            bar.next()
        index += 1
    bar.finish()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--directory", dest="directory", \
                        help="Path of configuration file")
    args = parser.parse_args()
    directory = args.directory if args.directory else "output"
    assert os.path.exists(directory), "Nonexistent directory"
    map_sites(directory)
