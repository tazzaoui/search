# wikisearch
> A search engine for the Wikipedia corpus

<div style="text-align:center"><img src ="screenshot.png" /></div>

## Features

1. Parser - Parses the most recent Wikipedia data dump & extracts the text from each article
* After pulling the Wikipedia data dump (~50 GB uncompressed), the parser extracts and saves each article to disk. The name of the file that contains an article is the hex-encoded title of the article.

2. Indexer - Builds an inverted index and computes the frequency of each token in every article. The tokenization process includes...
* Casefolding
* Stop Word Removal
* Stemming (PorterStemmer)

3. Search Ranker - Maps the search query along with each article to a k-dimensional vector space where k is the number of unique tokens in the corpus. In this mapping the i^th component of each vector is the tf-idf score of token i. Documents are then ranked with respect to their cosine similarity to the search query.
