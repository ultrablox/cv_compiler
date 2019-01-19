#!/usr/bin/env python3

import os
from skills_db import *
from log import *
from cv.employee_profile import *
import re
from projection import *
import argparse


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


def task_relevance(task, skill_table, skill_db):
  # Less skill you have - more focused you are
  # Take product of skill usage by their relevance and divide it by full task length
  # It's rough averaging, but looks good for now

  per_skill_time = 1.0 / len(task.skills)

  print_pairs = []
  component_relevance = [0.0] * len(task.skills)
  for i in range(0, len(task.skills)):
    component_relevance[i] = per_skill_time * skill_table[skill_db.find_skill(task.skills[i])]
    print_pairs += ['%s: %f' % (task.skills[i], component_relevance[i])]

  # log_print('; '.join(print_pairs))

  return sum(component_relevance)


def project_relevance(project):
  # (sum task_time * task_relevance ) / project_length
  relevant_timespan = sum((x.relevance * x.period.get_length()) for x in project.tasks)
  total_timespan = project.get_period().get_length()
  # print('Relevant=%f, total=%f' % (relevant_timespan, total_timespan))
  return relevant_timespan / total_timespan


def main():
  parser = argparse.ArgumentParser(description='Compile CV projection for given vacancy')
  parser.add_argument('vacancy_file', type=str, help='vacancy text file')
  parser.add_argument('input_dir', type=str, default='../sample_input', help='input profile directory')
  args = parser.parse_args()

  skill_db = SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  profile = EmployeeProfile(skill_db)
  # profile.load('../../my_cv/data')
  profile.load(args.input_dir)

  vacancy_text = get_text(args.vacancy_file)
  # print(vacancy_test)

  # Split by words
  matched_skills = []
  for skill in skill_db.skills:
    for syn in skill.get_synonims():
      if text_contains(vacancy_text, syn):
        log_print(LOG_LEVEL_DEBUG, 'Matched %s by "%s"' % (skill, syn))
        matched_skills += [skill]
        break

  print('Known skills in vacancy: %s' % ', '.join((str(x) for x in matched_skills)))
  for skill in matched_skills:
    skill_db.connect_to_matcher(skill)

  # Compute skill relevance
  skill_relevance = {}
  for skill_rec in profile.skillRecords:
    skill_ref = skill_rec.skill
    # print('%s' % skill_ref)
    relevance = skill_db.get_relevance(skill_ref)
    skill_relevance[skill_ref] = relevance
    skill_rec.relevance = relevance
    if relevance:
      log_print(LOG_LEVEL_DEBUG, 'Relevance %s: %f' % (skill_ref.name, relevance))

  # Compute tasks and project relevances
  for project in profile.projects:
    for task in project.tasks:
      task_assesment = task_relevance(task, skill_relevance, skill_db)
      task.relevance = task_assesment
      log_print(LOG_LEVEL_DEBUG, '%s -> %f' % (task, task.relevance))

    proj_assesment = project_relevance(project)
    project.relevance = proj_assesment
    log_print(LOG_LEVEL_DEBUG, '%s -> %f' % (project, proj_assesment))

  # Serialize to different folder
  cprsr = Compressor()
  relevant_profile = cprsr.create_relevant_projection(profile)
  relevant_profile.save_to('profile.analysed')


if __name__ == "__main__":
    main()
