
from cv.time import *
import datetime

class Task:
  def __init__(self):
    self.achievements = []

  def __str__(self):
    return self.description

  def deserialize(self, json_node, ctx):
    self.description = json_node['description']
    self.period = TimePeriod(json_node['period'])
    
    self.skills = []
    for skill_name in json_node['skills']:
      new_skill = ctx.skillDb.find_skill(skill_name, True)
      self.skills += [new_skill]

    if 'achievements' in json_node:
      self.achievements = json_node['achievements']

  def serialize(self):
    return {
      'description': self.description,
      'relevance': self.relevance,
      'skills': list(map(lambda x: x.name, self.skills)),
      'period': str(self.period),
      'achievements': self.achievements
    }

  def remove_skill(self, skill):
    if skill in self.skills:
      index = self.skills.index(skill)
      del self.skills[index]
