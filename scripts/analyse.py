#!/usr/bin/env python3
import os
from skills_db import *
from employee_profile import *
import re

def regex_escape(text):
  bad_symbols = ['+', '#']

  res = ''
  for symb in text:
    if symb in bad_symbols:
      res += '\\'
    res += symb
  return res

def get_text(file_path):
  with open(file_path, 'r') as f:
    return f.read()

def text_contains(vacancy_test, keyword):
  match = re.search(r'\W%s\W' % regex_escape(keyword), vacancy_test, flags=re.IGNORECASE)
  if match:
    return True
  else:
    return False

def main():
  skill_db = SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  profile = EmployeeProfile()
  profile.load('../../my_cv/data')


  vacancy_text = get_text('../test_data/vacancy_1.txt')
  # print(vacancy_test)

  # Split by words
  matched_skills = []
  for skill in skill_db.skills:
    for syn in skill.get_synonims():
      if text_contains(vacancy_text, syn):
        matched_skills += [skill]
        break

  print('Known skills in vacancy: %s' % ' '.join((str(x) for x in matched_skills)))
  for skill in matched_skills:
    skill_db.connect_to_matcher(skill)

  for employee_skill in profile.skills:
    skill_ref = skill_db.find_skill(employee_skill)
    if not skill_ref:
      log_print(LOG_LEVEL_WARNING, 'Skipping unkown skill: %s' % employee_skill)
    else:
      relevance = skill_db.get_relevance(skill_ref)
      if relevance:
        print('Relevance %s: %f' % (employee_skill, relevance))
  
  

if __name__ == "__main__":
    main()
