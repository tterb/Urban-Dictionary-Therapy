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

import sys, html, urllib.request, re, textwrap
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from random import randint

color = { 'PURPLE':'\033[95m', 'CYAN':'\033[96m', 'DARKCYAN':'\033[36m', 'BLUE':'\033[94m', 'GREEN':'\033[92m', 'YELLOW':'\033[93m', 'RED':'\033[91m', 'BOLD':'\033[1m', 'UNDERLINE':'\033[4m', 'END':'\033[0m' }

def form(s):
  if "win" in sys.platform:
    s[0] = '\nWord: '+str(s[0])
    s[1] = 'Def: '+str(s[1])
    s[2] = 'Ex: '+str(s[2])
    return '\n'.join(s)
  elif "linux" or "darwin" in sys.platform:
    # need to test compatability on OS X
    s[0] = color['PURPLE']+' \nWord: '+color['END']+s[0]
    s[1] = color['YELLOW']+' Def: '+color['END']+s[1]
    s[2] = color['DARKCYAN']+' Ex: '+color['END']+s[2]
    return '\n'.join(s)

def clean(s):
  s = '\n      '.join(s.split('<br/><br/>'))
  s = re.sub(re.compile('<.*?>'), '', s)
  s = html.unescape(html.unescape(s))
  if '\n' not in s:
    s = '\n      '.join(textwrap.wrap(s, 60, break_long_words=False))
  if '\"\"' in s:
    s = '\"'.join(s.split('\"\"'))
  return s

def scrape(url, index):
  page = urllib.request.urlopen(urllib.request.Request(url))
  soup = BeautifulSoup(page, "html.parser")
  term = []
  if index >= len(re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))):
    return None
  term.append(re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))[index][1].capitalize()) # Word
  term.append(clean(re.compile(r'<div class=\"meaning\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index].split('<br/> <br/>')[-1]).capitalize()) # Definition
  term.append(clean('\"'+re.compile(r'<div class=\"example\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index]+'\"')) # Example
  return term


def main():

  parser = ArgumentParser(description='Process some integers.')
  parser.add_argument('-s', '--search', help='Returns the definition for the provided term')
  parser.add_argument('-n', '--num', type=int, help='Returns (n) definitions for the provided term')
  parser.add_argument('-a', '--all', action='store_true', help='Returns all definitions for the provided term')
  parser.add_argument('-w', '--wotd', action='store_true', help='Returns the definition for the word of the day')
  args = parser.parse_args()
  print(vars(args))
  url = "https://www.urbandictionary.com/"
  term = []
  if args.num:
    index = args.num
  else:
    index = 6
  # if len(vars(args)) == 0:
  #   term = form(scrape(url, randint(0,index)))
  # else:
  if args.wotd:
    term.append(form(scrape(url, 0)))
  elif args.search:
    # if len(vars(args)) == 2:
    url += 'define.php?term='+args.search
    if args.all or args.num:
      # url += 'define.php?term='+args[-1]
      for i in range(0,index):
        data = scrape(url, i)
        if data != None:
          term.append(form(data))
        elif index > 0:
          sys.exit()
        else:
          print("I'm sorry, there is no data for the given term")
          sys.exit()
    else:
      term = scrape(url, randint(0,index))
      while term == None:
        index = index//2
        term = scrape(url, randint(0,index))
        if index == 0:
          print("I'm sorry, there is no data for the given term")
          sys.exit()
      term = form(term)
  elif args.all or args.num:
    term = []
    for i in range(0,index):
      term.append(form(scrape(url, i)))
  else: 
    term.append(form(scrape(url, randint(0,index))))
    
  for line in term:
    print(line)
  print('')
  sys.exit()
  

if __name__ == '__main__':
  main()
