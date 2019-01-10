#!/usr/bin/env python3
#!C:/Python36/python3
# UDTherapy.py

#*****************************************************************
# Urban Dictionary Therapy is a simple rehabilitation program for
# coping with those long frustrating days of programming. Utilizing
# this program and the information generously donated by the online
# community, you too can return to your work as a more successful,
# functioning member of society.
#*****************************************************************

import sys, html, re, textwrap
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from urllib import request
from random import randint
from colorama import init, Fore, Style


def main():
  init()
  parser = ArgumentParser(description='A simple rehabilitation program for coping with those long frustrating days of programming')
  parser.add_argument('-s', '--search', help='Returns the definition for the provided term')
  parser.add_argument('-n', '--num', type=int, help='Returns (n) definitions for the provided term')
  parser.add_argument('-a', '--all', action='store_true', help='Returns the first page of definitions for the provided term')
  parser.add_argument('-w', '--wotd', action='store_true', help='Returns the definition for the word of the day')
  args = parser.parse_args()

  term = []
  index = 6
  url = "https://www.urbandictionary.com/"
  if args.num and args.num < 6:
    index = args.num
  if args.wotd:
    term.append(scrape(url, 0))
  elif args.search:
    url += 'define.php?term='+args.search
    if args.all or args.num:
        for i in range(index):
          data = scrape(url, i)
          if data != None:
            term.append(data)
          else:
            print("I'm sorry, there is no data for the given term")
            sys.exit()
    else:
      term.append(scrape(url, randint(0,index)))
      while len(term) == 0:
        index = index//2
        term.append(scrape(url, randint(0,index)))
        if index == 0:
          print("I'm sorry, there is no data for the given term")
          sys.exit()
  elif args.all or args.num:
    [term.append(scrape(url, i)) for i in range(0,index)]
  else:
    term.append(scrape(url, randint(0,index)))
  [print(form(line)) for line in term]


def scrape(url, index):
  term = []
  page = request.urlopen(request.Request(url))
  soup = BeautifulSoup(page, "html.parser")
  if index >= len(re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))):
    return None
  term.append(re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))[index][1].capitalize()) # Word
  term.append(clean(re.compile(r'<div class=\"meaning\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index].split('<br/> <br/>')[-1]).capitalize()) # Definition
  term.append(clean('\"'+re.compile(r'<div class=\"example\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index]+'\"')) # Example
  return term


""" Formats and colors program output """
def form(term):
  if "linux" or "darwin" in sys.platform:
    term[0] = Fore.MAGENTA+' \nWord: '+Style.RESET_ALL+term[0]
    term[1] = Fore.YELLOW+' Def: '+Style.RESET_ALL+term[1]
    term[2] = Fore.CYAN+' Ex: '+Style.RESET_ALL+term[2]
  return '\n'.join(term)


""" Removes remaining HTML tags from term information """
def clean(term):
  term = '\n      '.join(term.split('<br/><br/>'))
  term = re.sub(re.compile('<.*?>'), '', term)
  term = term.replace('&amp;apos', '\'')
  term = html.unescape(html.unescape(term))
  if '\n' not in term:
    term = '\n      '.join(textwrap.wrap(term, 60, break_long_words=False))
  if '\"\"' in term:
    term = '\"'.join(term.split('\"\"'))
  return term


if __name__ == '__main__':
  main()
