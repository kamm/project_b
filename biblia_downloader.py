#!/usr/bin/python
# coding=iso-8859-2
# vim: set fileencoding=iso-8859-2

#import os
import urllib
import urllib2
from lxml import html

oldTes=[u'Rdz', 'Wj', 'Kpł', 'Lb', 'Pwt', 'Joz', 'Sdz', 'Rt', '1 Sm', '2 Sm', '1 Krl', '2 Krl', '1 Krn', '2 Krn', 'Ezd', 'Ne', 'Tb', 'Jdt', 'Est', '1 Mch', '2 Mch', 'Hi', 'Ps', 'Prz', 'Koh', 'Pnp', 'Mdr', 'Syr', 'Iz', 'Jr', 'Lm', 'Ba', 'Ez', 'Dn', 'Oz', 'Jl', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag', 'Za', 'Ml']
newTes=[u'Mt', 'Mk', 'Łk', 'J', 'Dz', 'Rz', '1 Kor', '2 Kor', 'Ga', 'Ef', 'Flp', 'Kol', '1 Tes', '2 Tes', '1 Tm', '2 Tm', 'Tt', 'Flm', 'Hbr', 'Jk', '1 P', '2 P', '1 J', '2 J', '3 J', 'Jud', 'Ap']

url='http://www.biblia.pl/otworz.php'
values={'ksiega':'Kol',
  'rozdzial':'1'}
data=urllib.urlencode(values)
response = urllib2.urlopen(urllib2.Request(url, data)).read()
doc = html.fromstring(response)
for data in doc.xpath('//div[@class="tresc"]'):
    tresc=''.join(data.xpath('.//span[@class="werset"]/text()'))
print tresc
