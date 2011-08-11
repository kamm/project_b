#!/usr/bin/python
# coding=iso-8859-2
# vim: set fileencoding=iso-8859-2

__license__ = 'GPL 3'
__copyright__ = '2011, Tomasz Dlugosz <tomek3d@gmail.com>'

#import os
import urllib
import urllib2
import re
from lxml import html
from lxml import etree

oldTes=[u'Rdz', 'Wj', 'Kpł', 'Lb', 'Pwt', 'Joz', 'Sdz', 'Rt', '1 Sm', '2 Sm', '1 Krl', '2 Krl', '1 Krn', '2 Krn', 'Ezd', 'Ne', 'Tb', 'Jdt', 'Est', '1 Mch', '2 Mch', 'Hi', 'Ps', 'Prz', 'Koh', 'Pnp', 'Mdr', 'Syr', 'Iz', 'Jr', 'Lm', 'Ba', 'Ez', 'Dn', 'Oz', 'Jl', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag', 'Za', 'Ml']
newTes=[u'Mt', 'Mk', 'Łk', 'J', 'Dz', 'Rz', '1 Kor', '2 Kor', 'Ga', 'Ef', 'Flp', 'Kol', '1 Tes', '2 Tes', '1 Tm', '2 Tm', 'Tt', 'Flm', 'Hbr', 'Jk', '1 P', '2 P', '1 J', '2 J', '3 J', 'Jud', 'Ap']

class Book:
    def __init__(self):
        self.footnotes={}
        self.content=""

    def GetBook(self, book):
        counter = 1
        while True:
            url='http://www.biblia.deon.pl/otworz.php'
            values={'ksiega': book,
              'rozdzial': str(counter)}
            data=urllib.urlencode(values)
            response = urllib2.urlopen(urllib2.Request(url, data)).read()
            doc = html.fromstring(response)

            if counter == 1:
                BookTitle = (doc.findall('.//span[@style="font-size:22px;"]')[0])
                self.content += html.tostring(BookTitle)
                ChaptersInBook = len(doc.findall('.//select[@name="rozdzial"]/option'))

            Book.GetContent(self, doc.xpath('//div[@class="tresc"]')[0], counter)
            Book.GetFootnotes(self, doc.xpath('//td[@width="150"]/table/tr[5]/td/div[1]')[0], counter)

            if counter == ChaptersInBook:
                # add footnotes here
                break
            counter += 1


    def GetFootnotes(self, doc, ChapterNo):
        chapterFootnotes = {}
        for ppp in html.tostring(doc).split(r'<a name="P') :
            footnote = ppp.partition('"><b>')
            verse = str(ChapterNo) + re.sub(r'^[^#]*#', '', footnote[0])
            if verse[0] != 'W' :
                continue
            chapterFootnotes[verse] = footnote[2].partition(' -  ')[2]
            self.footnotes = dict(self.footnotes.items() + chapterFootnotes.items())

    def GetContent(self, doc, counter):
        draft = html.tostring(doc)

        subs = (
        # remove gif spacer
            (r'<img src="gfx/null.gif".*?>', r''),
        # fix anchor name
            (r'<a name="', r'<a name="' + str(counter)),
        # fix footnote link
            (r'<a href="/rozdzial.php\?id=.*?#P', r'<a href="#' + str(counter) + r'P')
        )

        for fromPattern, toPattern in subs:
            draft = re.sub(fromPattern, toPattern, draft)
        self.content += draft

    def PrintBookContent(self):
        print self.content

#parser = etree.XMLParser()
#parser.feed("<root/>")

#root = parser.close()
#print etree.tostring(root)

test = Book()
test.GetBook('Kol')
test.PrintBookContent()
