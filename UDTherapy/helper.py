#!/usr/bin/env python3

"""
Urban Dictionary Therapy
A simple rehabilitation program for coping with long days of programming.
Utilizing this program and the information generously donated by the online
community, you too can return to your work as a more successful, functioning
member of society.
UDTherapy/helper.py
Brett Stevenson (c) 2017
"""

import sys, html, re, textwrap, argparse
from bs4 import BeautifulSoup
from urllib import request
from colorama import Fore, Style


""" Parses command-line options """
def parse_options(args):
  parser = argparse.ArgumentParser(prog='Urban Dictionary Therapy', description='A simple rehabilitation program for coping with long days of programming', usage='%(prog)s [options]', add_help=True)
  parser.add_argument('-s', '--search', nargs='+', help='display the definition for the provided term', default='')
  parser.add_argument('-n', '--num', type=int, help='specify the number of definitions to display', default=1)
  parser.add_argument('-a', '--all', action='store_true', help='display the first page of definitions for the provided term')
  parser.add_argument('-w', '--wotd', action='store_true', help='display the definition for the word of the day')
  parser.add_argument('-v', '--version', action='version', version='v1.0.1', help='show the program version number and exit')
  return parser.parse_args(args)


""" Returns the target URL """
def generate_url(args):
  url = 'https://www.urbandictionary.com/'
  if args.search:
    url += 'define.php?term='+'%20'.join(args.search)
  return url


""" Retrieves data for the term at the given index """
def scrape_term(url, index):
  term = []
  soup = BeautifulSoup(request.urlopen(request.Request(url)), 'html.parser')
  results = re.findall(r'<a class="word" href=\"(.*?)\">(.*?)</a>', str(soup.findAll('a')))
  if not len(results):
    return None
  elif index >= len(results):
    index = len(results)-1
  term.append(results[index][1].capitalize()) # Word
  term.append(clean(re.compile(r'<div class=\"meaning\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index].split('<br/> <br/>')[-1]).capitalize()) # Definition
  term.append(clean('\"'+re.compile(r'<div class=\"example\">(.*?)</div>', re.S).findall(str(soup.findAll('div')).replace('\n', ''))[index]+'\"')) # Example
  return term


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


""" Formats and colors program output """
def format(term):
  if 'linux' or 'darwin' in sys.platform:
    term[0] = Fore.RED+' Word: '+Style.RESET_ALL+term[0]
    term[1] = Fore.CYAN+' Def: '+Style.RESET_ALL+term[1]
    term[2] = Fore.YELLOW+' Ex: '+Style.RESET_ALL+term[2]
  return '\n'.join(term)+'\n'