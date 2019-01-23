#!/usr/bin/env python3

import os
from db import skills_db
from cv.employee_profile import *
import re
from projection import *
import argparse
import logging
import math
from datetime import datetime





def task_relevance(task, skill_table, skill_db, vacancy_skill_count):
  # Less skill you have - more focused you are
  # Take product of skill usage by their relevance and divide it by full task length
  # It's rough averaging, but looks good for now

  # per_skill_time = 1.0 / len(task.skills)
  # print_pairs = []
  # component_relevance = [0.0] * len(task.skills)
  # for i in range(0, len(task.skills)):
  #   component_relevance[i] = per_skill_time * skill_table[skill_db.find_skill(task.skills[i])]
  #   print_pairs += ['%s: %f' % (task.skills[i], component_relevance[i])]
  # res = sum(component_relevance)
  
  # Check intersection with vacancy requirements
  res = 0.0
  for skill in task.skills:
    res += skill_table[skill]
  res = res / vacancy_skill_count
  
  if task.achievements:
    res = res * 1.2
  # print(skill_table)
  
  # Check how long time passed since then
  # After 5 years (T) relevance becomes 1/4 (R)
  # r(t) = exp(-k*t), k = - ln(R)/T
  t1 = (datetime.today() - task.period.endDate).days
  t2 = (datetime.today() - task.period.startDate).days

  print('t1=%f, t2=%f' % (t1, t2))

  T = 5*365.0
  R = 0.25
  k = - math.log(R) / T
  # print(k)

  elapsed_rel = (math.exp(-k*t1) - math.exp(-k * t2)) / (k *(t2 - t1))
  
  # print(elapsed_rel)
  res *= elapsed_rel
  # exit(1)

  assert res <= 1.0, 'Task relevance cant exceed 1.0'
  # log_print('; '.join(print_pairs))

  return res


def project_relevance(project):
  # (sum task_time * task_relevance ) / project_length
  # relevant_timespan = sum((x.relevance * x.period.get_length()) for x in project.tasks)
  # total_timespan = project.get_period().get_length()
  # res = relevant_timespan / total_timespan
  res = max(x.relevance for x in project.tasks)
  
  # Nobody believes that hobby projects worth discussing...
  # ..except me
  if not project.parent:
    res = 0.7 * res

  assert res <= 1.0, 'Relevance cant exceed 1.0'
  return res

def employment_relevance(employment):
  return max(x.relevance for x in employment.projects)


def main():
  logging.basicConfig(level=logging.INFO)

  parser = argparse.ArgumentParser(description='Compile CV projection for given vacancy')
  parser.add_argument('input_dir', type=str, default='../sample_input', help='input profile directory')
  parser.add_argument('skills', type=str, help='skills text file')
  args = parser.parse_args()

  skill_db = skills_db.SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  profile = EmployeeProfile(skill_db)
  profile.load(args.input_dir)

  matched_skills = [skill_db.find_skill(x) for x in get_text(args.skills).strip().split('\n')]
 
  logging.info('Matching with skills: %s' % matched_skills)
  
  for skill in matched_skills:
    skill_db.connect_to_matcher(skill)

  vacancy_skill_count = len(matched_skills)

  # Compute skill relevance
  logging.info('Skill Relevances:')
  skill_relevance = {}
  for skill_rec in profile.skillRecords:
    skill_ref = skill_rec.skill
    # print('%s' % skill_ref)
    relevance = skill_db.get_relevance(skill_ref)
    skill_relevance[skill_ref] = relevance
    skill_rec.relevance = relevance
    if relevance:
      logging.info('::: %s: %f' % (skill_ref.name, relevance))

  # Compute tasks and project relevances
  for project in profile.projects:
    logging.info('Checking tasks for "%s" project:' % project.name)
    for task in project.tasks:
      task_assesment = task_relevance(task, skill_relevance, skill_db, vacancy_skill_count)
      task.relevance = task_assesment
      logging.info('::: %s -> %f' % (task, task.relevance))

    proj_assesment = project_relevance(project)
    project.relevance = proj_assesment


  # Compute employments relevances
  logging.info('Employments relevance:')
  for employment in profile.employments:
    employment.relevance = employment_relevance(employment)
    logging.info('::: %s -> %f' % (employment.name, employment.relevance))

  # Serialize to different folder
  cprsr = Compressor()
  relevant_profile = cprsr.create_relevant_projection(profile, 0.07)
  
  logging.info('Project relevance:')

  for prj in relevant_profile.projects:
    logging.info('===Relevance for %s: %f' % (prj, prj.relevance))

  relevant_profile.save_to('profile.analysed')
  # exit(1)


if __name__ == "__main__":
    main()
