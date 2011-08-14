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

oldTes=[u'Rdz', 'Wj', 'Kp�', 'Lb', 'Pwt', 'Joz', 'Sdz', 'Rt', '1 Sm', '2 Sm', '1 Krl', '2 Krl', '1 Krn', '2 Krn', 'Ezd', 'Ne', 'Tb', 'Jdt', 'Est', '1 Mch', '2 Mch', 'Hi', 'Ps', 'Prz', 'Koh', 'Pnp', 'Mdr', 'Syr', 'Iz', 'Jr', 'Lm', 'Ba', 'Ez', 'Dn', 'Oz', 'Jl', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag', 'Za', 'Ml']
newTes=[u'Mt', 'Mk', '�k', 'J', 'Dz', 'Rz', '1 Kor', '2 Kor', 'Ga', 'Ef', 'Flp', 'Kol', '1 Tes', '2 Tes', '1 Tm', '2 Tm', 'Tt', 'Flm', 'Hbr', 'Jk', '1 P', '2 P', '1 J', '2 J', '3 J', 'Jud', 'Ap']
css = '''
<style type="text/css">
    .miedzytytul1 {font-weight:bold; color:#0099cf; text-align:center; font-size:14px;}
    .przypis {color:#0000ff; font-weight:bold; font-size:11px;}
    .werset {font-weight:bold; font-size:15px; color:#000000;}
</style>
'''
doctype = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >'

class Book:
    def __init__(self):
        self.footnotes=""
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

            prefix = book + ' ' + str(counter)
            Book.GetContent(self, doc.xpath('//div[@class="tresc"]')[0], prefix)
            Book.GetFootnotes(self, doc.xpath('//td[@width="150"]/table/tr[5]/td/div[1]')[0], prefix)

            if counter == ChaptersInBook:
                self.content += '<br><br>' + self.footnotes
                break
            counter += 1


    def GetFootnotes(self, doc, prefix):
        chapterFootnotes = ""
        for ppp in html.tostring(doc).split(r'<a name="P') :
            footnote = ppp.partition('"><b>')
            footnoteNo = footnote[0].partition('"')[0]
            verse = re.sub(r'^[^#]*#', '', footnote[0])
            if verse[0] != 'W' :
                continue
            footnoteText = re.sub(r'otworz\.php\?skrot=', r'#', footnote[2].partition(' -  ')[2])
            footnoteText = re.sub(r'skrot', r'przypis', footnoteText)
            verse = re.sub('W', ',', verse)
            chapterFootnotes += '<a id="' + prefix + 'P' + footnoteNo + '" href="#' + prefix + verse + '" class="przypis"> [' + prefix + verse + ']</a> ' + footnoteText + ' \n'

        self.footnotes += chapterFootnotes

    def GetContent(self, doc, prefix):
        draft = html.tostring(doc)

        subs = (
        # remove gif spacer
            (r'<img src="gfx/null.gif".*?>', r''),
        # remove 'relative' divs
            (r'position:relative; ', r''),
        # fix anchor name
            (r'<a name="W', r'<a name="' + prefix + ','),
        # fix footnote link
            (r'<a href="/rozdzial.php\?id=.*?#P', r'<a href="#' + prefix + r'P')
        )

        for fromPattern, toPattern in subs:
            draft = re.sub(fromPattern, toPattern, draft)
        self.content += draft

    def PrintBookContent(self):
        print self.content

test = Book()
test.GetBook('Ag')
print doctype
print "<html>"
print "<head>"
print css
print "</head>"
test.PrintBookContent()
print "</html>"
