#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import logging
import base64
import datetime
from random import randint
from argparse import ArgumentParser
from collections import deque
from threading import Thread, Lock
from lxml import html
from lxml.cssselect import CSSSelector
from pybloomfilter import BloomFilter

count = 0
failures = 0


def parse_url(url, proxy=None, save_dir="."):
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
    h = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0)\
            Gecko/20100101 Firefox/10.0', 'Accept-Language': 'en-US', }
    url = str(url, "utf-8") if not isinstance(url, str) else url
    save_dir = str(save_dir,
                   "utf-8") if not isinstance(save_dir,
                                              str) else save_dir
    while status != 200 and attempts > 0:
        try:
            r = requests.get(url, headers=h, proxies=proxy)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(
                "[tid {}] URL: {} Error Msg: {}".format(
                    tid, url, str(e)))
            return urls
        status = r.status_code
        attempts -= 1
    if attempts > 0:
        dest = os.path.join(save_dir.encode(), base64.b16encode(url.encode()))
        with open(dest, "w") as f:
            f.write(r.text)
        dom = html.fromstring(r.text)
        dom.make_links_absolute(url, resolve_base_href=True)
        anchor_selector = CSSSelector('a')
        urls = [str(e.get('href')) for e in anchor_selector(dom)]
    return urls


def threaded_crawl(tid, n, proxies, lock, output_dir="."):
    global count
    global failures
    fails = 0
    logger = logging.getLogger(__name__)
    fptr = open("top-1m.csv", "r")
    fail_thresh = 10  # Use a different proxy after 10 failed requests in a row
    proxy = dict()
    linum = fails = 0
    start = tid * n   # First seed site to crawl
    end = tid * n + n  # Last seed site to crawl
    seed = BloomFilter(n * 1000000, 0.1, '/tmp/{}.bloom'.format(tid).encode())
    frontier = deque()
    logger.info('[tid {}] Loading seed URLs {} - {}'.format(tid, start, end))
    for line in fptr:
        if linum >= start and linum < end:
            url = "http://" + line.split(',')[1].strip()
            seed.add(url.encode())
            frontier.append(url)
        linum += 1
    fptr.close()
    while True:
        url = frontier.popleft()
        urls = []
        try:
            urls = parse_url(url, proxy, output_dir)
        except Exception as e:
            logger.error(
                "[tid {}] Fatal error occured while crawling: {}.".format(
                    tid, url))
        if len(urls) == 0:
            with lock:
                failures += 1
            fails += 1
            if fails > fail_thresh:
                proxy['http'] = proxies[randint(0, len(proxies) - 1)]
                logger.error(
                    "[tid {}] Failure: Activating proxy:{}".format(
                        tid, proxy['http']))
                fails = 0
        for u in urls:
            link = u.encode()
            if link not in seed:
                seed.add(link)
                frontier.append(link)
        with lock:
            count += 1
            if(count % 1000 == 0):
                logger.info('Page count: {}'.format(count))
        if len(frontier) % 1000 == 0:
            logger.info(
                "[tid {}] Frontier count: {}".format(
                    tid, len(frontier)))


def main(num_threads, seed, output_dir):
    logging.basicConfig(filename="{}.log".format(str(datetime.datetime.now())),
                        level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    logger = logging.getLogger(__name__)
    logging.info("Generating proxy list...")
    os.system('curl\
    "http://pubproxy.com/api/proxy?limit=100&format=txt&http=true&country=US&type=http"\
    -o proxy-list.txt')
    with open('proxy-list.txt', 'r') as f:
        proxies = [x.strip() for x in f.readlines()]
    lock = Lock()
    for i in range(num_threads):
        thread = Thread(target=threaded_crawl,
                        args=(i, seed / num_threads, proxies, lock, output_dir))
        logger.info("Launching thread {}\n".format(i))
        thread.start()
    for i in range(num_threads):
        thread.join()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--threads", dest="num_threads",
                        help="number of threads to spawn")
    parser.add_argument("-n", "--num-seeds", dest="seed",
                        help="the number of links to use for the initial seed")
    parser.add_argument("-o", "--output-dir", dest="output_dir",
                        help="directory in which to dump data throughout the crawl")
    args = parser.parse_args()
    num_threads = int(args.num_threads) if args.num_threads else 5
    seed = int(args.seed) if args.seed else 1000
    output_dir = args.output_dir if args.output_dir else "."
    main(num_threads, seed, output_dir)
