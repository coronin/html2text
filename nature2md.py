#!/usr/bin/env python
'''nature2md: turn current nature issue page into Markdown-structured text'''
__version__ = '1'
__author__ = 'Liang Cai (i@cailiang.net)'

tag='test'
#import time
#tag = 'nature_%s' % time.strftime('%Y-%m-%d-%H%M')
import os
os.system('[ -f %s.html ] || /usr/bin/wget http://www.nature.com/nature/current_issue.html -O %s.html' % (tag,tag) )

from bs4 import BeautifulSoup
soup = BeautifulSoup( open('%s.html' % tag, 'r'), 'lxml' )
for tag in soup.find_all("a", href="#top"):
    tag.decompose()
for tag in soup.find_all("abbr", class_="open-access"):
    tag.decompose()
a = soup.find_all("div", class_="section")
b = '![](http://www.nature.com/%s)' % soup.find(
      "div", class_="sub-inner-content" ).img["src"]
for tag in a:
    if tag["id"] in ('research', 'comment', 'news-in-focus', 'special'):
        b += '\n\n%s' % tag.div.div.prettify()
#### buggy

import html2text
h = html2text.HTML2Text()
#h.ignore_links = True
#h.ignore_images = True
c = h.handle(b)
d = c.replace('](/', '](http://www.nature.com/'
    ).replace('    * ', '    '
    ).replace('  * #  [', '### ['
    )
print d

import urllib
import urllib2
SCKEY = open('SCKEY.txt', 'r').read().strip()
url = 'http://sc.ftqq.com/%s.send' % SCKEY
values = { 'text': 'Nature, %s' % tag,
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
