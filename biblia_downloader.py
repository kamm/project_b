#!/usr/bin/python
# coding=iso-8859-2
# vim: set fileencoding=iso-8859-2

#import os
import urllib
import urllib2
import re
from lxml import html

oldTes=[u'Rdz', 'Wj', 'Kpł', 'Lb', 'Pwt', 'Joz', 'Sdz', 'Rt', '1 Sm', '2 Sm', '1 Krl', '2 Krl', '1 Krn', '2 Krn', 'Ezd', 'Ne', 'Tb', 'Jdt', 'Est', '1 Mch', '2 Mch', 'Hi', 'Ps', 'Prz', 'Koh', 'Pnp', 'Mdr', 'Syr', 'Iz', 'Jr', 'Lm', 'Ba', 'Ez', 'Dn', 'Oz', 'Jl', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag', 'Za', 'Ml']
newTes=[u'Mt', 'Mk', 'Łk', 'J', 'Dz', 'Rz', '1 Kor', '2 Kor', 'Ga', 'Ef', 'Flp', 'Kol', '1 Tes', '2 Tes', '1 Tm', '2 Tm', 'Tt', 'Flm', 'Hbr', 'Jk', '1 P', '2 P', '1 J', '2 J', '3 J', 'Jud', 'Ap']

url='http://www.biblia.pl/otworz.php'
values={'ksiega':'Kol',
  'rozdzial':'1'}
data=urllib.urlencode(values)
response = urllib2.urlopen(urllib2.Request(url, data)).read()
doc = html.fromstring(response)
footnotes = {}
for pdata in doc.xpath('//td[@width="150"]/table/tr[5]/td/div[1]'):
    for ppp in html.tostring(pdata).split(r'<a name="P') :
        footnote = ppp.partition('"><b>')
        verse = re.sub(r'^[^#]*#', '', footnote[0])
        if verse[0] != 'W' :
            continue
        footnotes[verse] = footnote[2].partition(' -  ')[2]

'''
for k, v in footnotes.iteritems():
     print k, v
'''
bookTitle = (doc.findall('.//span[@style="font-size:22px;"]')[0].text)
ChaptersInBook = len(doc.findall('.//select[@name="rozdzial"]/option'))
'''
for data in doc.xpath('//div[@class="tresc"]'):
    tresc=''.join(data.xpath('.//span[@class="werset"]/text()'))
print tresc
'''
