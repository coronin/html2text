#!/usr/bin/env python
'''cell2md: turn current cell issue page into Markdown-structured text'''
__version__ = '1.1'
__author__ = 'Liang Cai (i@cailiang.net)'
# TODO:
# download
# send to sc.ftqq.com

from bs4 import BeautifulSoup
soup = BeautifulSoup( open("test.html", 'r'), 'lxml' )
a = soup.select("ol.articleCitations")
b = a[0].prettify()

import html2text
h = html2text.HTML2Text()
#h.ignore_links = True
#h.ignore_images = True
c = h.handle(b)

import time
import urllib
import urllib2
SCKEY = open('SCKEY.txt', 'r').strip()
url = 'http://sc.ftqq.com/%s.send' % SCKEY
values = { 'text': "current issue of Cell %s" % time.strftime('%Y/%m/%d'),
           'desp': unicode(c).encode('utf-8') }
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
resp = urllib2.urlopen(req)
json = resp.read()
print json
