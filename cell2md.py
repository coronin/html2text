#!/usr/bin/env python
'''cell2md: turn current cell issue page into Markdown-structured text'''
__version__ = '1.2.1'
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
h.ignore_links = True
#h.ignore_images = True
c = h.handle(b)
d = c.replace('\n\nIn Brief  Summary  Full-Text HTML  PDF', ''
    ).replace('\n\nIn Brief  Summary  PDF', ''
    ).replace('](/', '](http://www.cell.com/'
    ).replace('x ', '>'
    ).replace('![Abstract ', '----\n\n![Abstract '
    ).replace('.sml)\n\n', '.sml)\n\n### '
    ).replace('> (Cell', '(Cell')

import time
import urllib
import urllib2
SCKEY = open('SCKEY.txt', 'r').read().strip()
url = 'http://sc.ftqq.com/%s.send' % SCKEY
values = { 'text': "Cell, %s" % time.strftime('%Y/%m/%d %H:%M'),
           'desp': unicode(d).encode('utf-8') }
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
resp = urllib2.urlopen(req)

import json
z = json.loads( resp.read() )
if z['errno'] == 0:
    print unicode(z['errmsg'])
elif z['errno']:
    print z['errno']
    print unicode(z['errmsg'])
else:
    print json.dumps(z)
