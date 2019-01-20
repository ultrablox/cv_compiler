#!/usr/bin/env python3

# Sample usage:
# ./extract_skills.py ../test_data/vacancy_7.txt > ../test_data/skills_7.txt

import logging
import os
import argparse
import re
from skills_db import *
from utils import *


def regex_escape(text):
  bad_symbols = ['+', '#']

  res = ''
  for symb in text:
    if symb in bad_symbols:
      res += '\\'
    res += symb
  return res


def text_contains(vacancy_test, keyword):
  match = re.search(r'\W%s\W' % regex_escape(keyword), vacancy_test, flags=re.IGNORECASE)
  if match:
    return True
  else:
    return False

def main():
  logging.basicConfig(level=logging.ERROR)

  parser = argparse.ArgumentParser(description='Extract skills from vacancy text')
  parser.add_argument('vacancy_file', type=str, help='vacancy text file')
  args = parser.parse_args()

  assert os.path.exists(args.vacancy_file), 'File with text does not exist'

  skill_db = SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  vacancy_text = get_text(args.vacancy_file)

  matched_skills = []
  for skill in skill_db.skills:
    for syn in skill.get_synonims():
      if text_contains(vacancy_text, syn):
        logging.debug('Matched %s by "%s"' % (skill, syn))
        matched_skills += [skill]
        break

  print('\n'.join((str(x.name) for x in matched_skills)))


if __name__ == "__main__":
    main()
