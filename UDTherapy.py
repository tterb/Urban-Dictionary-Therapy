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

import sys, urllib.request, re, random
from bs4 import BeautifulSoup

url = "https://www.urbandictionary.com/"
page = urllib.request.urlopen(urllib.request.Request(url))
soup = BeautifulSoup(page, "html.parser")
index = random.randint(0,6)
word = re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))[index][1]
definition = re.compile(r'<div class=\"meaning\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index]
example = re.compile(r'<div class=\"example\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index]
print('Word:', str(word))
print('Def: ', str(definition))
print("\n\""+str(example)+"\"")
