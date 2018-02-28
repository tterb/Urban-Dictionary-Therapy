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

import sys, html, re, textwrap
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from urllib import request
from random import randint

color = { 'PURPLE':'\033[95m', 'CYAN':'\033[96m', 'DARKCYAN':'\033[36m', 'BLUE':'\033[94m', 'GREEN':'\033[92m', 'YELLOW':'\033[93m', 'RED':'\033[91m', 'BOLD':'\033[1m', 'UNDERLINE':'\033[4m', 'END':'\033[0m' }

def main():
  parser = ArgumentParser(description='A simple rehabilitation program for coping with those long frustrating days of programming')
  parser.add_argument('-s', '--search', help='Returns the definition for the provided term')
  parser.add_argument('-n', '--num', type=int, help='Returns (n) definitions for the provided term')
  parser.add_argument('-a', '--all', action='store_true', help='Returns all definitions for the provided term')
  parser.add_argument('-w', '--wotd', action='store_true', help='Returns the definition for the word of the day')
  args = parser.parse_args()

  url = "https://www.urbandictionary.com/"
  term = []
  if args.num:
    index = args.num
  else:
    index = 6
  if args.wotd:
    term.append(form(scrape(url, 0)))
  elif args.search:
    url += 'define.php?term='+args.search
    if args.all or args.num:
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
    for i in range(0,index):
      term.append(form(scrape(url, i)))
  else: 
    term.append(form(scrape(url, randint(0,index))))
    
  for line in term:
    print(line)
  print('')
  sys.exit()


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
  

""" Formats the program output """
def form(term):
  if "win" in sys.platform:
    term[0] = '\nWord: '+str(term[0])
    term[1] = 'Def: '+str(term[1])
    term[2] = 'Ex: '+str(term[2])
  elif "linux" or "darwin" in sys.platform:
    # need to test compatability on macOS
    term[0] = color['PURPLE']+' \nWord: '+color['END']+term[0]
    term[1] = color['YELLOW']+' Def: '+color['END']+term[1]
    term[2] = color['DARKCYAN']+' Ex: '+color['END']+term[2]
  return '\n'.join(term)


""" Removes remaining HTML tags from term information """
def clean(term):
  term = '\n      '.join(term.split('<br/><br/>'))
  term = re.sub(re.compile('<.*?>'), '', term)
  term = html.unescape(html.unescape(term))
  if '\n' not in term:
    term = '\n      '.join(textwrap.wrap(term, 60, break_long_words=False))
  if '\"\"' in term:
    term = '\"'.join(term.split('\"\"'))
  return term


if __name__ == '__main__':
  main()
