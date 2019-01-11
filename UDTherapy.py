#!/usr/bin/env python3
#!C:/Python36/python3

"""
Urban Dictionary Therapy
A simple rehabilitation program for coping with long days of programming.
Utilizing this program and the information generously donated by the online
community, you too can return to your work as a more successful, functioning
member of society.
UDTherapy.py
Brett Stevenson (c) 2017
"""

import sys, html, re, textwrap, argparse 
from bs4 import BeautifulSoup
from urllib import request
from random import randrange
from colorama import init, Fore, Style


def main(args):
  init()
  term, index = [], 6
  args = parse_options(args)
  url = generate_url(args)
  if args.num and args.num < 6:
    index = args.num
  if args.wotd:
    term.append(scrape_term(url, 0))
  elif args.all or args.num:
    [term.append(scrape_term(url, i)) for i in range(0, index)]
  else:
    term.append(scrape_term(url, randrange(index)))
  if not len(term) and args.search:
    print("I'm sorry, there is no data for the given term")
    sys.exit()
  [print(form(line)) for line in term]


def parse_options(args):
  parser = argparse.ArgumentParser(prog='Urban Dictionary Therapy', description='A simple rehabilitation program for coping with those long days', usage='%(prog)s [options]', add_help=True)
  parser.add_argument('-s', '--search', help='Returns the definition for the provided term')
  parser.add_argument('-n', '--num', type=int, help='Returns (n) definitions for the provided term')
  parser.add_argument('-a', '--all', action='store_true', help='Returns the first page of definitions for the provided term')
  parser.add_argument('-w', '--wotd', action='store_true', help='Returns the definition for the word of the day')
  return parser.parse_args(args)


""" Returns the target URL """
def generate_url(args):
  url = 'https://www.urbandictionary.com/'
  if args.search:
    url += 'define.php?term='+args.search
  return url


""" Retrieves data for the term at the given index """
def scrape_term(url, index):
  term = []
  soup = BeautifulSoup(request.urlopen(request.Request(url)), "html.parser")
  if not len(results):
    return None
  elif index >= len(results):
    index = len(results)-1
  term.append(results[index][1].capitalize()) # Word
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
  term = '\n\t\t'.join(term.split('<br/><br/>'))
  term = re.sub(re.compile('<.*?>'), '', term)
  term = term.replace('&amp;apos', '\'')
  term = html.unescape(html.unescape(term))
  if '\n' not in term:
    term = '\n      '.join(textwrap.wrap(term, 60, break_long_words=False))
  if '\"\"' in term:
    term = '\"'.join(term.split('\"\"'))
  return term


if __name__ == '__main__':
  main(sys.argv[1:])
