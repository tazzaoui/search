#!/usr/bin/env bash

# This script pulls the wikipedia corpus from 
# http://www.cs.upc.edu/~nlp/wikicorpus/
# and tokenizes each article

rm -rf ../indexer/index
rm -rf ../indexer/raw
rm -rf ../indexer/tokenized-raw

echo "Downloading raw data..."
mkdir -p ../indexer/docs
cd ../indexer/docs
wget http://www.cs.upc.edu/~nlp/wikicorpus/raw.en.tgz
tar -xvf raw.en.tgz
rm raw.en.tgz 
cd ../../support

echo "Extracting articles..."
./extract.py

echo "Tokenizing articles..."
./tokinze_articles.py
rm -rf ../indexer/raw
mv ../indexer/tokenized-raw ../indexer/raw
