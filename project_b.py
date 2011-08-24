#!/usr/bin/python
# coding=utf-8

__license__ = 'GPL 3'
__copyright__ = '2011, Tomasz Długosz <tomek3d@gmail.com>'

#import os
import sys
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
        self.footnotes=[]
        self.content=[]
        counter = 1
        while True:
            url='http://www.biblia.deon.pl/otworz.php'
            values={'ksiega': book.decode('utf-8').encode('iso8859_2'),
              'rozdzial': str(counter)}
            data=urllib.urlencode(values)
            response = urllib2.urlopen(urllib2.Request(url, data)).read()
            doc = html.fromstring(response)

            if counter == 1:
                BookTitle = (doc.findall('.//span[@style="font-size:22px;"]')[0])
                self.content.append(re.sub(r'</span>', r'</div>', re.sub(r'<span style=\"font-size:22px;\"',r'<br><br><a name="' + book.decode('utf-8').encode('iso8859_2') + r'"></a><div class="tytul"', html.tostring(BookTitle))))
                ChaptersInBook = len(doc.findall('.//select[@name="rozdzial"]/option'))
            else:
                self.content.append('<br><br>')

            prefix = book.decode('utf-8').encode('iso8859_2') + ' ' + str(counter)
            self.content.append('<div class="numer">' + str(counter) + '</div>')
            Book.GetContent(self, doc.xpath('//div[@class="tresc"]')[0], prefix)
            Book.GetFootnotes(self, doc.xpath('//td[@width="150"]/table/tr[5]/td/div[1]')[0], prefix)

            if counter == ChaptersInBook:
                self.content.append('<br><br>' + "".join(self.footnotes))
                break
            counter += 1


    def GetFootnotes(self, doc, prefix):
        chapterFootnotes = []
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
            # one newline is enough
                (r'<br><br>', r'<br>')
            )

            for fromPattern, toPattern in subs:
                footnoteText = re.sub(fromPattern, toPattern, footnoteText)

            verse = re.sub('W', ',', verse)
            chapterFootnotes.append('<a id="' + prefix + 'P' + footnoteNo + '" href="#' + prefix + verse + '" class="przypis"> [' + prefix + verse + ']</a> ' + footnoteText)

        self.footnotes.append("\n".join(chapterFootnotes))

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
        self.content.append(draft)

    def PrintBookContent(self):
        print "".join(self.content)

def usage():
    print
    print "Wspierane parametry: stary, nowy, wszystko, <nazwa księgi>"
    print "stary \t\t- pobiera Stary Testament"
    print "nowy \t\t- pobiera Nowy Testament"
    print "wszystko \t- pobiera Stary i Nowy Testament"
    print "<nazwa księgi> \t- pobiera jedną księgę, np. 'Rdz' lub '1 Kor'"

def ToC(testament, books):
    url='http://biblia.deon.pl/index.php'
    response = urllib2.urlopen(url).read()
    doc = html.fromstring(response)
    for entry, href in zip(doc.xpath('.//tr[@valign="top"][' + testament + ']/td/a'), books):
        print re.sub(r'class=\"ks\" href=\".*?\"', r'href="#' + href.decode('utf-8').encode('iso8859_2') + r'"', html.tostring(entry)) + '<br>'
    print '<br><br>'

def main(task):
    print doctype
    print "<html>"
    print "<head>"
    print meta
    print title.decode('utf-8').encode('iso8859_2')
    print css
    print "</head>"
    target = []
    if task in ['wszystko', 'stary']:
        print '<div class="tytul">STARY TESTAMENT</div><br><br>'
        ToC('1', oldTes)
        target.extend(oldTes)
    if task in ['wszystko', 'nowy']:
        print '<div class="tytul">NOWY TESTAMENT</div><br><br>'
        ToC('2', newTes)
        target.extend(newTes)
    if task in oldTes or task in newTes:
        target.append(task)
    singleBook = Book()
    for book in target:
        singleBook.GetBook(book)
        singleBook.PrintBookContent()
    print "</html>"

if len(sys.argv) != 2:
    print "Podaj 1 argument"
    usage()
    sys.exit(1)
if sys.argv[1] in oldTes or sys.argv[1] in newTes or sys.argv[1] in ['stary', 'nowy', 'wszystko']:
    main(sys.argv[1])
else:
    print "Nieprawidłowy argument"
    usage()
    sys.exit(1)

