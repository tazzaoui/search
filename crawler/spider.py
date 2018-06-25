#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import logging
import time
import chardet
import base64
from argparse import ArgumentParser
from collections import deque
from threading import Thread
from lxml import etree, cssselect, html
from pybloomfilter import BloomFilter
from requests.exceptions import ConnectionError

def parse_url(url, save_dir="."):
    '''
    - Parses the contents of a single page and returns a
      list of the URLs it contains.
    - Saves the document as an html file under save_dir with
      the base16 encoding of the corresponding URL as the filename
    - Returns an empty list after 5 unsuccessful connection attempts.
    '''
    attempts = 5
    status = 0
    urls = []
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0)\
            Gecko/20100101 Firefox/10.0', 'Accept-Language':'en-US',})
    while status != 200 and attempts > 0:
        try:
            r = requests.get(url, headers=headers)
        except Exception as e:
            logger = logging.getLogger('__main__')
            logger.error("[{}] {}".format(url, str(e)))
            return urls
        status = r.status_code
        attempts -= 1
    if attempts > 0:
        content = r.text.encode()
        encoding = chardet.detect(content)['encoding']
        if encoding != 'utf-8' and hasattr(content, 'encode'):
            content = content.decode(encoding, 'replace').encode('utf-8')
        path = os.path.join(save_dir.encode(), base64.b16encode(url.encode()))
        with open (path, "w") as f:
            f.write(r.text)
        data = html.document_fromstring(content)
        data.make_links_absolute(url, resolve_base_href=True)
        urls = data.xpath('//a/@href')
        for idx, item in enumerate(urls):
            if urls[idx][0] == '/':
                urls[idx] = url + urls[idx][1:]
    return urls

def threaded_crawl(tid, n, max_depth = 10, output_dir="."):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("[tid {}]".format(tid))
    fptr = open("top-1m.csv", "r")
    sentinel = "SENTINEL"
    depth = -1
    linum = 0
    start = tid*n       # First seed site to crawl
    end = tid*n + n     # Last seed site to crawl 
    seed = BloomFilter(n*max_depth*1000, 0.1, '/tmp/{}.bloom'.format(tid).encode())
    frontier = deque()
    frontier.append(sentinel)
    logger.info('Loading seed URLs {} - {}'.format(start, end))
    for line in fptr:
        if linum >= start and linum < end:
            url = "http://" + line.split(',')[1].strip()
            seed.add(url.encode())
            frontier.append(url)
        linum += 1
    fptr.close()
    while depth < max_depth:
        url = frontier.popleft()
        urls = []
        if url == sentinel:
            depth += 1
            logger.info('Depth = {}'.format(depth))
            frontier.append(sentinel)
            url = frontier.popleft()
        try:
            urls = parse_url(url, output_dir)
        except Exception as e:
            logger.error("[{}] Fatal error occured while crawling.".format(url))
        logger.info('Crawled {} & found {} links'.format(url, len(urls)))
        for u in urls:
            link = u.encode()
            if link not in seed:
                seed.add(link)
                frontier.append(link)
        logger.info('Frontier: {}'.format(len(frontier)))

def main(num_threads, seed, max_depth, output_dir):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    for i in range(num_threads):
        thread = Thread(target = threaded_crawl,\
                args=(i, seed/num_threads,max_depth, output_dir))
        logger.info("Launching thread {}\n".format(i))
        thread.start()
    for i in range(num_threads):
        thread.join()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--threads", dest="num_threads", \
            help="number of threads to spawn")
    parser.add_argument("-n", "--num-seeds", dest="seed", \
            help="the number of links to use for the initial seed")
    parser.add_argument("-d", "--max-depth", dest="max_depth", \
            help="the maximum depth of links to crawl")
    parser.add_argument("-o", "--output-dir", dest="output_dir",\
            help="directory in which to dump data throughout the crawl")
    args = parser.parse_args()
    num_threads = int(args.num_threads) if args.num_threads else 5
    seed = int(args.seed) if args.seed else 1000
    max_depth = int(args.max_depth) if args.max_depth else 10
    output_dir = args.output_dir if args.output_dir else "."
    main(num_threads, seed, max_depth, output_dir)
