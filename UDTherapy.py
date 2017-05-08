#!C:/Python36/python
#/usr/bin/env python3
# UrbanDicTherapy.py

#*****************************************************************
# Urban Dictionary Therapy is a simple rehabilitation program for
# coping with those long frustrating days of programming. Utilizing
# this program and the information generously donated by the online
# community, you too can return to your work as a more successful,
# functioning member of society.
#*****************************************************************

import sys, html, urllib.request, re, textwrap, random
from bs4 import BeautifulSoup
from sys import platform

color = { 'PURPLE':'\033[95m', 'CYAN':'\033[96m', 'DARKCYAN':'\033[36m', 'BLUE':'\033[94m', 'GREEN':'\033[92m', 'YELLOW':'\033[93m', 'RED':'\033[91m', 'BOLD':'\033[1m', 'UNDERLINE':'\033[4m', 'END':'\033[0m' }

def clean(s):
    s = "\n     ".join(s.split("<br/><br/>"))
    s = re.sub(re.compile('<.*?>'), '', s)
    s = html.unescape(html.unescape(s))
    if '\n' not in s:
        s = '\n     '.join(textwrap.wrap(s, 75, break_long_words=False))
    if '\"\"' in s:
        s = '\"'.join(s.split('\"\"'))
    return s

def format(s):
    if "win" in platform:
        s[0] = 'Word:'+str(s[0])
        s[1] = 'Def:'+str(s[1])
        s[2] = 'Ex:'+str(s[2])
        return s
    elif "linux" in platform or "darwin" in platform:
        # need to test OS X
        s[0] = color['PURPLE']+'Word: '+color['END']+s[0]
        s[1] = color['YELLOW']+'Def: '+color['END']+s[1]
        s[2] = color['DARKCYAN']+'Ex: '+color['END']+s[2]
        return s

def scrape(soup, index):
    term = []
    term.append(re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))[index][1].capitalize()) # Word
    term.append(clean(re.compile(r'<div class=\"meaning\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index].capitalize())) # Definition
    term.append(clean('\"'+re.compile(r'<div class=\"example\">(.*?)</div>', re.S).findall(str(soup.findAll('div')))[index]+'\"')) # Example
    return term

def main():
    url = "https://www.urbandictionary.com/"
    page = urllib.request.urlopen(urllib.request.Request(url))
    soup = BeautifulSoup(page, "html.parser")
    print('')
    if len(sys.argv) <= 1:
        term = scrape(soup, random.randint(0,6))
        for line in format(term):
            print(line)
        print('')
    elif len(sys.argv) > 1:
        if '-a' in sys.argv[1] or '--all' in sys.argv[1]:
            for i in range(0,6):
                for line in format(scrape(soup, i)):
                    print(line)
                print('')
    sys.exit()

if __name__ == '__main__':
    main()
