from db import skills_db
import os
import re
import logging


class SkillReference:
  def __init__(self, skill, pos, len):
    self.skill = skill
    self.pos = pos
    self.len = len
  
  def name(self):
    return self.skill.name

class Analyzer:
  def __init__(self):
    self._matchedSkills = []

    self._skillDb = skills_db.SkillsDB()
    script_dir = os.path.dirname(os.path.realpath(__file__)) 
    self._skillDb.load(os.path.join(script_dir, os.pardir, os.pardir, 'database'))
  
  def _regex_escape(self, text):
    bad_symbols = ['+', '#']

    res = ''
    for symb in text:
      if symb in bad_symbols:
        res += '\\'
      res += symb
    return res


  def _text_contains(self, vacancy_test, keyword):
    match = re.search(r'\W%s\W' % self._regex_escape(keyword), vacancy_test, flags=re.IGNORECASE)
    if match:
      span = match.span(0)
      return True, span[0], span[1]
    else:
      return False, 0, 0

  def parse(self, text):
    for skill in self._skillDb.skills:
      for syn in skill.get_synonims():
        matched, first, last = self._text_contains(text, syn)
        if matched:
          logging.debug(r'Matched {} by "{}" ({}-{})'.format(skill, syn, first, last))
          self._matchedSkills += [SkillReference(skill, first, last - first)]
          break

  def matched_names(self):
    return sorted([s.name() for s in self._matchedSkills])

  def matched_skills(self):
    return self._matchedSkills
