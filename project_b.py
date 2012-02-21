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

oldTes=[u'Rdz', u'Wj', u'Kpł', u'Lb', u'Pwt', u'Joz', u'Sdz', u'Rt', u'1 Sm', u'2 Sm', u'1 Krl', u'2 Krl', u'1 Krn', u'2 Krn', u'Ezd', u'Ne', u'Tb', u'Jdt', u'Est', u'1 Mch', u'2 Mch', u'Hi', u'Ps', u'Prz', u'Koh', u'Pnp', u'Mdr', u'Syr', u'Iz', u'Jr', u'Lm', u'Ba', u'Ez', u'Dn', u'Oz', u'Jl', u'Am', u'Ab', u'Jon', u'Mi', u'Na', u'Ha', u'So', u'Ag', u'Za', u'Ml']
newTes=[u'Mt', u'Mk', u'Łk', u'J', u'Dz', u'Rz', u'1 Kor', u'2 Kor', u'Ga', u'Ef', u'Flp', u'Kol', u'1 Tes', u'2 Tes', u'1 Tm', u'2 Tm', u'Tt', u'Flm', u'Hbr', u'Jk', u'1 P', u'2 P', u'1 J', u'2 J', u'3 J', u'Jud', u'Ap']
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
title = u'<title>Pismo Święte</title>'

class Book:
    def GetBook(self, book):
        self.footnotes=[]
        self.content=[]
        counter = 1
        plainBook = unicodeToPlain(book)
        while True:
            url='http://www.biblia.deon.pl/otworz.php'
            values={'ksiega': book.encode('iso8859_2'),
              'rozdzial': str(counter)}
            data=urllib.urlencode(values)
            response = urllib2.urlopen(urllib2.Request(url, data)).read()
            doc = html.fromstring(response)

            if counter == 1:
                BookTitle = (doc.findall('.//span[@style="font-size:22px;"]')[0])
                self.content.append(re.sub(r'</span>', r'</div>', re.sub(r'<span style=\"font-size:22px;\"',r'<br><br><a name="K' + plainBook + r'"></a><div class="tytul"', html.tostring(BookTitle))))
                ChaptersInBook = len(doc.findall('.//select[@name="rozdzial"]/option'))
            else:
                self.content.append('<br><br>')

            plainPrefix = plainBook + str(counter)
            self.content.append('<div class="numer">' + str(counter) + '</div>')
            Book.GetContent(self, doc.xpath('//div[@class="tresc"]')[0], plainPrefix)
            Book.GetFootnotes(self, doc.xpath('//td[@width="150"]/table/tr[5]/td/div[1]')[0], plainPrefix, unicodeToReference(book) + ' ' + str(counter))

            if counter == ChaptersInBook:
                self.content.append('<br><br>' + "".join(self.footnotes))
                break
            counter += 1


    def GetFootnotes(self, doc, plainPrefix, prefix):
        chapterFootnotes = []
        for ppp in html.tostring(doc).split(r'<a name="P') :
            footnote = ppp.partition('"><b>')
            footnoteNo = footnote[0].partition('"')[0]
            verse = re.sub(r'^[^#]*#', '', footnote[0])
            if verse[0] != 'W' :
                continue
            footnoteText = re.sub(r'otworz\.php\?skrot=', r'#W', footnote[2].partition(' - ')[2]).strip()

            subs = (
            # remove trailing whitespaces
                (r'\s+<br>', r'<br>'),
            # change class name
                (r'skrot', r'przypis'),
            # fix href
                ('%20', ''),
                ('%C5%821', 'l'),
                ('%C5%822', 'L'),
            # one newline is enough
                (r'<br><br>', r'<br>'),
            # <div> tags were not open
                (r'<br></div>', r'<br>')
            )

            for fromPattern, toPattern in subs:
                footnoteText = re.sub(fromPattern, toPattern, footnoteText)

            verse = re.sub('W', ',', verse)
            chapterFootnotes.append('<a id="P' + plainPrefix + 'P' + footnoteNo + '" href="#W' + plainPrefix + verse + '" class="przypis"> [' + prefix + verse + ']</a> ' + footnoteText)
            #chapterFootnotes.append('<a id="' + plainPrefix + 'P' + footnoteNo + '" href="#' + plainPrefix + verse + '" class="przypis"> [' + plainPrefix + verse + ']</a> ' + footnoteText)

        self.footnotes.append("\n".join(chapterFootnotes))

    def GetContent(self, doc, plainPrefix):
        draft = html.tostring(doc)

        subs = (
        # remove gif spacer
            (r'<img src="gfx/null.gif".*?>', r''),
        # remove huge chapter numbers
            (r'<div align=\"left\" style=\"font-size:48px; color:#0099cf; top:40px; position:relative; font-weight:bold; margin:0px;\">[0-9]*</div>', r''),
        # fix anchor name
            (r'<a name="W', r'<a name="W' + plainPrefix + ','),
        # fix footnote link
            (r'<a href="/rozdzial.php\?id=.*?#P', r'<a href="#P' + plainPrefix + r'P'),
        # remove trailing whitespaces
            (r'\s+<br>', r'<br>')
        )

        for fromPattern, toPattern in subs:
            draft = re.sub(fromPattern, toPattern, draft)
        self.content.append(draft)

    def PrintBookContent(self):
        print "".join(self.content)

def unicodeToPlain(text):
    subs = (
    # remove whitespaces
        (' ', ''),
    # replace non-ascii chars
        (u'ł','l'),
        (u'Ł', 'L')
    )
    for fromPattern, toPattern in subs:
        text = re.sub(fromPattern, toPattern, text)
    return text

def unicodeToReference(text):
    subs = (
    # replace non-ascii chars
        (u'ł','&#321;'),
        (u'Ł', '&#322;')
    )
    for fromPattern, toPattern in subs:
        text = re.sub(fromPattern, toPattern, text)
    return text

def usage():
    print
    print "Wspierane parametry: stary, nowy, wszystko, lista, <nazwa księgi>"
    print "stary \t\t- pobiera Stary Testament"
    print "nowy \t\t- pobiera Nowy Testament"
    print "wszystko \t- pobiera Stary i Nowy Testament"
    print "lista \t\t- wyświetla listę skróconych nazw ksiąg Starego i Nowego Testamentu"
    print "<nazwa księgi> \t- pobiera jedną księgę, np. 'Rdz' lub '1 Kor'"

def showList():
    print "księgi Starego Testamentu:"
    print "\t".join(oldTes).encode('utf-8')
    print "księgi Nowego Testamentu:"
    print "\t".join(newTes).encode('utf-8')

def ToC(testament, books):
    url='http://biblia.deon.pl/index.php'
    response = urllib2.urlopen(url).read()
    doc = html.fromstring(response)
    for entry, href in zip(doc.xpath('.//tr[@valign="top"][' + testament + ']/td/a'), books):
        print re.sub(r'class=\"ks\" href=\".*?\"', r'href="#K' + unicodeToPlain(href) + r'"', html.tostring(entry)) + '<br>'
    print '<br><br>'

def main(task):
    print doctype
    print "<html>"
    print "<head>"
    print meta
    print title.encode('iso8859_2')
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
task = sys.argv[1].decode('utf-8')
if task == "lista":
    showList()
elif task in oldTes or task in newTes or task in ['stary', 'nowy', 'wszystko']:
    main(task)
else:
    print "Nieprawidłowy argument"
    usage()
    sys.exit(1)

