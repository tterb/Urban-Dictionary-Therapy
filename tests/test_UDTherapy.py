#!/usr/bin/env python3

"""
Urban Dictionary Therapy
A simple rehabilitation program for coping with long days of programming.
Utilizing this program and the information generously donated by the online
community, you too can return to your work as a more successful, functioning
member of society.
tests/test_UDTherapy.py
Brett Stevenson (c) 2017
"""

import os, pytest
from UDTherapy import helper

@pytest.fixture
def test_data():
  return { 'opts': ['-s','udt'],
           'url': 'https://www.urbandictionary.com/define.php?term=udt', }

def test_arguments():
  args = helper.parse_options(['-s','udt','-n','3'])
  assert (args.search == 'udt' and args.num == 3) and not (args.all and args.wotd)

def test_generate_url(test_data):
  args = helper.parse_options(test_data['opts'])
  test_data['args'] = args
  assert helper.generate_url(args) == test_data['url']

def test_scrape_term(test_data):
  url = test_data['url']
  assert len(helper.scrape_term(url, 0))