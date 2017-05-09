#!/usr/bin/env python3
#!C:/Python36/python3
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

def form(s):
    if "win" in platform:
        s[0] = 'Word: '+str(s[0])
        s[1] = 'Def: '+str(s[1])
        s[2] = 'Ex: '+str(s[2])
        return s
    elif "linux" in platform or "darwin" in platform:
        # need to test compatability on OS X
        s[0] = color['PURPLE']+' Word: '+color['END']+s[0]
        s[1] = color['YELLOW']+' Def: '+color['END']+s[1]
        s[2] = color['DARKCYAN']+' Ex: '+color['END']+s[2]
        return s

def clean(s):
    s = '\n      '.join(s.split('<br/><br/>'))
    s = re.sub(re.compile('<.*?>'), '', s)
    s = html.unescape(html.unescape(s))
    if '\n' not in s:
        s = '\n      '.join(textwrap.wrap(s, 70, break_long_words=False))
    if '\"\"' in s:
        s = '\"'.join(s.split('\"\"'))
    return s

def scrape(url, index):
    page = urllib.request.urlopen(urllib.request.Request(url))
    soup = BeautifulSoup(page, "html.parser")
    term = []
    term.append(re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))[index][1].capitalize()) # Word
    term.append(clean(re.compile(r'<div class=\"meaning\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index].split('<br/> <br/>')[-1]).capitalize()) # Definition
    term.append(clean('\"'+re.compile(r'<div class=\"example\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index]+'\"')) # Example
    return term


def main(args):
    url = "https://www.urbandictionary.com/"
    if len(args) == 0:
        term = form(scrape(url, random.randint(0,6)))
    elif len(args) >= 1:
        if '-s' in args or '--search' in args:
            if len(args) >= 2:
                url += 'define.php?term='+args[-1]
                if '-a' in args or '--all' in args:
                    term = []
                    for i in range(0,6):
                        term.append(form(scrape(url, i)))
                else:
                    term = form(scrape(url, random.randint(0,6)))
            else:
                print("**ERROR**: The 's' argument requires that you specify a search term.")
                sys.exit()
        # elif '-l' in args or '--letter' in args:
        #     if len(args) >= 2:
        #         url += 'popular.php?character='+args[-1].upper()
        #         if '-a' in args or '--all' in args:
        #             term = []
        #             for i in range(0,6):
        #                 term.append(form(scrape(url, i)))
        #         else:
        #             term = form(scrape(url, random.randint(0,6)))
        #     else:
        #         print("**ERROR**: The '-l' argument requires that you specify an additional argument.")
        #         sys.exit()
        elif len(args) == 1 and ('-a' in args or '--all' in args):
            term = []
            for i in range(0,6):
                term.append(form(scrape(url, i)))
        elif len(args) == 1 and '-wotd' in args:
            term = form(scrape(url, 0))

        if '-h' in args[0] or '--help' in args[0]:
            f = '     {0:15} {1:75}'
            print('\n   Arguments:')
            print(f.format('-s or --search:', 'Prints a definition for the specified <term>'))
            print(f.format('-a or --all:', 'Prints the entire page of definitions'))
            print(f.format('-h or --help:', 'Prints a list of accepted arguments and their functionality'))
            print('')
    print('')
    for line in term:
        if type(line) is not list:
            print(line)
        else:
            print('')
            for n in line:
                print(n)
    print('')
    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
