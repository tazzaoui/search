#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
- This script defines a mapping between documents and document ids
- It then saves this mapping into a mysql database whose configuration
  is to be specified in a yaml file passed through the command line
  (see db-config.yml).
'''

import os
import sys
import pymysql
import yaml
from argparse import ArgumentParser

def map_sites(path, config):
    with open(config) as f:
        cfg = yaml.load(f)

    # Connect to the database
    connection = pymysql.connect(host=cfg['host'],
                                user=cfg['user'],
                                db=cfg['db_name'],
                                charset="utf8",
                                autocommit=True,
                                use_unicode=True,
                                cursorclass=pymysql.cursors.DictCursor)

    document_dir = os.fsencode(path)
    index = 0

    for document in os.listdir(document_dir):
        filename = os.fsdecode(document)
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Site-Map` (`ID`, `URL`) VALUES ('%s','%s');"
            #print(sql % (index, filename))
            cursor.execute(sql % (index, filename))
            index += 1

    connection.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", \
            help="Path of configuration file")
    parser.add_argument("-d", "--directory", dest="directory", \
            help="Path of configuration file")
    args = parser.parse_args()
    config = args.config if args.config else "db-config.yml"
    directory = args.directory if args.directory else "output"
    assert os.path.exists(config), "Nonexistent configuration file"
    map_sites(directory, config)
