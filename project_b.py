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

oldTes=[u'Rdz', 'Wj', 'Kpł', 'Lb', 'Pwt', 'Joz', 'Sdz', 'Rt', '1 Sm', '2 Sm', '1 Krl', '2 Krl', '1 Krn', '2 Krn', 'Ezd', 'Ne', 'Tb', 'Jdt', 'Est', '1 Mch', '2 Mch', 'Hi', 'Ps', 'Prz', 'Koh', 'Pnp', 'Mdr', 'Syr', 'Iz', 'Jr', 'Lm', 'Ba', 'Ez', 'Dn', 'Oz', 'Jl', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag', 'Za', 'Ml']
newTes=[u'Mt', 'Mk', 'Łk', 'J', 'Dz', 'Rz', '1 Kor', '2 Kor', 'Ga', 'Ef', 'Flp', 'Kol', '1 Tes', '2 Tes', '1 Tm', '2 Tm', 'Tt', 'Flm', 'Hbr', 'Jk', '1 P', '2 P', '1 J', '2 J', '3 J', 'Jud', 'Ap']
css = '''
<style type="text/css">
    .tresc {font-size:14px; margin-left:10px; line-height:20px;}
    .tytul {font-size:22px; font-weight:bold; color:#0099cf; text-align:center;}
    .tytul1 {font-size:16px; font-weight:bold; color:#0099cf; text-align:center;}
    .tytul2 {font-size:18px; text-align:center;}
    .numer {text-align:center; font-size:30px; color:#0099cf; font-weight:bold;}
    .miedzytytul1 {font-weight:bold; color:#0099cf; text-align:center; font-size:14px;}
    .miedzytytul2 {font-style:italic; text-align:center;}
    .miedzytytul3 {font-style:italic; font-size:12px; margin-left:-10px}
    .przypis {color:#0000ff; font-weight:bold; font-size:11px;}
    .werset {font-weight:bold; font-size:15px; color:#000000;}
</style>
'''
doctype = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >'
meta = '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-2" >'
title = '<title>Pismo Święte</title>'

class Book:
    def GetBook(self, book):
        self.footnotes=""
        self.content=""
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
                self.content += re.sub(r'</span>', r'</div>', re.sub(r'<span style=\"font-size:22px;\"',r'<br><br><a name="' + book + r'"></a><div class="tytul"', html.tostring(BookTitle))) 
                ChaptersInBook = len(doc.findall('.//select[@name="rozdzial"]/option'))
            else:
                self.content += '<br><br>'

            prefix = book + ' ' + str(counter)
            self.content += '<div class="numer">' + str(counter) + '</div>'
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
            footnoteText = re.sub(r'otworz\.php\?skrot=', r'#', footnote[2].partition(' - ')[2]).strip()

            subs = (
            # remove trailing whitespaces
                (r'\s+<br>', r'<br>'),
            # change class name
                (r'skrot', r'przypis'),
            # fix broken tag in source
                (r' <i dan>', r''),
            # one newline is enough
                (r'<br><br>', r'<br>')
            )

            for fromPattern, toPattern in subs:
                footnoteText = re.sub(fromPattern, toPattern, footnoteText)

            verse = re.sub('W', ',', verse)
            chapterFootnotes += '<a id="' + prefix + 'P' + footnoteNo + '" href="#' + prefix + verse + '" class="przypis"> [' + prefix + verse + ']</a> ' + footnoteText + ' \n'

        self.footnotes += chapterFootnotes

    def GetContent(self, doc, prefix):
        draft = html.tostring(doc)

        subs = (
        # remove gif spacer
            (r'<img src="gfx/null.gif".*?>', r''),
        # remove huge chapter numbers
            (r'<div align=\"left\" style=\"font-size:48px; color:#0099cf; top:40px; position:relative; font-weight:bold; margin:0px;\">[0-9]*</div>', r''),
        # fix anchor name
            (r'<a name="W', r'<a name="' + prefix + ','),
        # fix footnote link
            (r'<a href="/rozdzial.php\?id=.*?#P', r'<a href="#' + prefix + r'P'),
        # remove trailing whitespaces
            (r'\s+<br>', r'<br>')
        )

        for fromPattern, toPattern in subs:
            draft = re.sub(fromPattern, toPattern, draft)
        self.content += draft

    def PrintBookContent(self):
        print self.content

def ToC(testament):
    if testament == 'old':
        i = '1'
        print '<div class="tytul">STARY TESTAMENT</div><br><br>'
        books = oldTes
    else:
        i = '2'
        print '<div class="tytul">NOWY TESTAMENT</div><br><br>'
        books = newTes
    url='http://biblia.deon.pl/index.php'
    response = urllib2.urlopen(url).read()
    doc = html.fromstring(response)
    index = 0
    for bookList in doc.xpath('.//tr[@valign="top"][' + i + ']/td/a'):
        print re.sub(r'class=\"ks\" href=\".*?\"', r'href="#' + books[index] + r'"', html.tostring(bookList)) + '<br>'
        index+=1
    print '<br><br>'

test = Book()
print doctype
print "<html>"
print "<head>"
print meta
print title
print css
print "</head>"
ToC('old')
for book in oldTes:
    test.GetBook(book)
    test.PrintBookContent()
    #print book
print "</html>"
