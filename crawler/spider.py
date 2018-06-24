import hashlib
import requests
import logging
import multiprocessing
from lxml import etree, cssselect, html
from pybloomfilter import BloomFilter

def parse_url(url):
    '''
    - Parses the contents of a single page and returns a
      list of the URLs it contains.
    - Returns None after 5 unsuccessful connection attempts.
    '''
    attempts = 5
    status = 0
    urls = None
    while status != 200 and attempts > 0:
        r = requests.get(url)
        status = r.status_code
        attempts -= 1
    if attempts > 0:
        data = html.fromstring(r.text)
        data.make_links_absolute(url, resolve_base_href=True)
        urls = data.xpath('//a/@href')
        for idx, item in enumerate(urls):
            if urls[idx][0] == '/':
                urls[idx] = url + urls[idx][1:]
    return urls

def main():
   pass

if __name__ == '__main__':
    urls = crawl("http://gnu.org")
    print(urls)

