
from cv.time import *
import datetime

class Task:
  def __init__(self):
    self.achievements = []

  def __str__(self):
    return self.description

  def deserialize(self, json_node):
    self.description = json_node['description']
    self.period = TimePeriod(json_node['period'])
    self.skills = json_node['skills']
    if 'achievements' in json_node:
      self.achievements = json_node['achievements']

  def serialize(self):
    return {
      'description': self.description,
      'relevance': self.relevance,
      'skills': self.skills,
      'period': str(self.period),
      'achievements': self.achievements
    }

