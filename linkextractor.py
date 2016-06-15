#coding:utf8
from bs4 import BeautifulSoup
import requests
import json
import re
from eventlet.green import urllib2
import urlparse

class Crawler():
    def __init__(self,base_url,url):
        self.url = url
        self.base_url = base_url
        self.headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset' : 'utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
            'Referer' : self.base_url,
        }
        self.max_urls = 100

    def extract_links(self):
        source = self.get_site(url)
        soup = BeautifulSoup(source.text,"html.parser")
        links = soup.findAll('a')

        good_links = []
        for link in links:

            # Ignore anchor tags without href
            try:
                partial_link_url = str(link['href'])
            except KeyError:
                continue

            # Concatenate relative urls like "../joing.html" with currently being processed url
            link_url = urlparse.urljoin(url, partial_link_url)

            # Strip off any trailing jibberish like ?test=1
            (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(link_url)
            fragments = (scheme, netloc, path, '', '', '')
            link_url = urlparse.urlunparse(fragments)

            # Make sure we're still on the same domain
            (base_scheme, base_netloc, base_path, base_params, base_query, base_fragment) = urlparse.urlparse(url)

            if netloc != base_netloc:
                # Different domain
                pass
            else:
                # Add this link to the list
                if link_url not in good_links:
                    good_links.append(link_url)

        self.fileWriter(good_links)

    def soup(self,plain_text):
        return BeautifulSoup(plain_text,"html.parser")

    def get_site(self,url):
        return requests.get(self.url,headers=self.headers, timeout=10)

    def fileWriter(self,data):
        with open('urls.json', 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    base_url = "http://hamrogsm.com/"    
    url = "http://blog.hamrogsm.com/"
    crawler = Crawler(base_url,url)
    # extract link from a single page
    crawler.extract_links()
