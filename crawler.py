#coding:utf8
from bs4 import BeautifulSoup
import requests
import json
import re

class Crawler():
    """
    A crawler that fetches the latest ads from 
    site : http://hamrobazaar.com/
    with input keyword
    to output json in format:
        [{
            "price" : "",
            "ad_url" : "",
            "user_profile" : "",
            "title" : ""
        }]
    Note: to be used for eduactional purpose only
    """
    def __init__(self,base_url,url,depth):
        self.depth = depth #depth of pages to crawl
        self.offset = 0 #content offset in a page
        self.page = 0
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

    def next_page(self):
        """
        Paging offset for the search pages
        """
        self.offset+=20
        self.page+=1

    def crawl(self):
        data = []
        while self.page< self.depth:
            try:
                self.url = self.url+"&offset="+str(self.offset)
                source = self.get_site(url)
                soup = self.soup(source.text)
                for td in soup.findAll('td', attrs={'height': '115','bgcolor':'#F2F4F9'}):
                    block = {}
                    title = td.find('font',{'style':'font-size:15px;font-family:Arial, Helvetica, sans-serif;'})
                    if title:
                        block["title"] = title.text
                    for link in td.findAll('a'):
                        href = link.get("href")
                        if re.search("useritems.php?",href):
                            block["user_profile"] = "http://hamrobazaar.com/" + href
                        else:
                            block["ad_url"] = "http://hamrobazaar.com/" + href

                    while td:
                        td = td.findNext('td',{'width':'100',"bgcolor":"#F2F4F9"})
                        if td:
                            block["price"] = td.find("b").text

                    data.append(block)
            except Exception as e:
                print e

            self.next_page()
        self.fileWriter(data)

    def soup(self,plain_text):
        return BeautifulSoup(plain_text,"html.parser")

    def get_site(self,url):
        return requests.get(self.url,headers=self.headers, timeout=10)

    def fileWriter(self,data):
        with open('urls.json', 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    base_url = "http://hamrobazaar.com/"
    url = "http://hamrobazaar.com/search.php?do_search=Search"
    keyword = "guitar"
    search_keyword_url = url + "&searchword=" + keyword
    
    crawler = Crawler(base_url,search_keyword_url,5)
    crawler.crawl()