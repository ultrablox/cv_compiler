#!/usr/bin/env python3

# Sample usage:
# ./extract_skills.py ../test_data/vacancy_7.txt > ../test_data/skills_7.txt

import logging
import os
import argparse
import re
import sys
from db import skills_db
from utils import *
from vacancy_analyzer import analyzer


def main():
  logging.basicConfig(level=logging.ERROR)

  parser = argparse.ArgumentParser(description='Extract skills from vacancy text')
  parser.add_argument('vacancy_file', type=str, help='vacancy text file')
  args = parser.parse_args()

  assert os.path.exists(args.vacancy_file), 'File with text does not exist'

  vacancy_text = get_text(args.vacancy_file)

  v_analyzer = analyzer.Analyzer()
  v_analyzer.parse(vacancy_text)

  # print('\n'.join(v_analyzer.matched_names()))

  app = QtWidgets.QApplication(sys.argv)
  wnd = ParsedVacancyWindow()
  wnd.textEdit.setPlainText(vacancy_text)

  for skill in v_analyzer.matched_skills():
    wnd.flash_skill(skill.pos, skill.len)

  wnd.show()
  sys.exit(app.exec_())


if __name__ == "__main__":
    main()
