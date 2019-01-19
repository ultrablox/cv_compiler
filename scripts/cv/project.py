
from cv.task import *
from utils import *
import copy

class Project:
  def __init__(self):
    self.parent = None
    self.linesOfCode = None
    self.webLink = ''
    self.icon = ''
    self.visible = True
    self.tasks = []
    self.notes = []

  def serialize(self):
    res = {
      'name': self.name,
      'description': self.description,
      'team-size': self.teamSize,
      'relevance': self.relevance,
      'visible': self.visible,
      'notes': self.notes,
      'web' : self.webLink
    }

    serialize_array_to_property(res, 'tasks', self.tasks)
    return res

  def deserialize(self, prj_node):
    self.name = prj_node['name']
    self.description = prj_node['description']
    self.teamSize = prj_node['team-size']

    if 'code_size' in prj_node:
      self.linesOfCode = prj_node['code_size']

    if 'icon' in prj_node:
        self.icon = prj_node['icon']

    if 'web' in prj_node:
        self.webLink = prj_node['web']

    # self.skills = []
    # if 'skills' in prj_node:
    #     for skill in prj_node['skills']:
    #         self.skills += [skill]

    # if 'secondary_skills' in prj_node:
    #     for skill in prj_node['secondary_skills']:
    #         self.skills += [skill['name']]

    if 'notes' in prj_node:
        self.notes += [prj_node['notes']]

    for task_node in prj_node['tasks']:
      new_task = Task()
      new_task.deserialize(task_node)
      self.tasks += [new_task]

    if 'period' in prj_node:
      self.period = TimePeriod(prj_node['period'])

    if 'visible' in prj_node:
      self.visible = prj_node['visible']

  def get_total_skill_list(self):
    res = []
    # res += self.skills
    for task in self.tasks:
      res += task.skills

    return sorted(set(res))

  def get_period(self):
    if self.tasks:
      res = copy.deepcopy(self.tasks[0].period)
      for i in range(1, len(self.tasks)):
        res.startDate = min(res.startDate, self.tasks[i].period.startDate)
        res.endDate = max(res.endDate, self.tasks[i].period.endDate)
      return res
    else:
      return self.period

  def __str__(self):
    return self.name
