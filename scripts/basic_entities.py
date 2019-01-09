
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


from skill_attitude import *
from utils import *
from log import *
from check import *
import datetime
import copy


class TimePeriod:
  DATE_FORMAT = '%d.%m.%Y'

  def __init__(self, data):
    interval = data.split('-')
    self.startDate = datetime.datetime.strptime(interval[0], TimePeriod.DATE_FORMAT)

    if interval[1] == 'now':
      self.endDate = datetime.datetime.now()
      self.isOpen = True
    else:
      self.endDate = datetime.datetime.strptime(interval[1], TimePeriod.DATE_FORMAT)

      self.isOpen = False

    check_always(self.startDate < self.endDate, 'Invalid time period : %s' % self)

  def __str__(self):
    start = self.startDate.strftime(TimePeriod.DATE_FORMAT)
    end = 'now' if self.isOpen else self.endDate.strftime(TimePeriod.DATE_FORMAT)
    return '%s-%s' % (start, end)

  # Return days count in float
  def get_length(self):
    return (self.endDate - self.startDate).days


class DateIndexer:
  def __init__(self, min_date, max_date):
    self.minDate = min_date
    self.maxDate = max_date

  def month_count(self):
    return self.index(self.maxDate)

  def index(self, date):
    return (date.year - self.minDate.year) * 12 + (date.month - self.minDate.month)


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


class Project:
  def __init__(self):
    self.parent = None
    self.linesOfCode = None
    self.webLink = None
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
      'notes': self.notes
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


class SkillExperience:
  def __init__(self, skill_ref):
    self.periods = []
    self.skill = skill_ref
    self.attitude = SkillAttitude.NEUTRAL
    self.timespan = None
    self.relevance = 0.0

  def name_with_abbr(self):
    if self.name == self.fullName:
      return self.name
    else:
      return '%s (%s)' % (self.fullName, self.name)

  def serialize(self):
    return {
      'name': self.skill.name,
      'timespan': self.total_size(),
      'attitude': self.attitude,
      'relevance': self.relevance
    }

  def deserialize(self, json_node):
    self.timespan = json_node['timespan']
    self.attitude = json_node['attitude']
    self.relevance = json_node['relevance']

  def add_period(self, new_period):
    log_print(LOG_LEVEL_DEBUG, 'Adding period for %s: %s' % (self.skill.name, new_period))
    self.periods += [new_period]

  def total_size(self):
    if self.timespan:
      return self.timespan
    else:
      if len(self.periods) == 0:
        return 0.0
      else:
        min_date = self.periods[0].startDate
        max_date = self.periods[0].endDate

        for period in self.periods:
          min_date = min(min_date, period.startDate)
          max_date = max(max_date, period.endDate)

        di = DateIndexer(min_date, max_date)

        months = [0] * di.month_count()

        for period in self.periods:
            for idx in range(di.index(period.startDate), di.index(period.endDate)):
                months[idx] = 1

        return sum(1 for item in months if item == (1)) / 12.0


class Employment:
  def __init__(self):
    self.notes = []

  def deserialize(self, json_node, profile):
    self.name = json_node['name']
    self.period = TimePeriod(json_node['period'])
    self.web = json_node['web']
    self.role = json_node['role']
    self.description = json_node['description']
    self.logo = json_node['logo']
    if 'notes' in json_node:
      self.notes = json_node['notes']

    self.projects = []
    for prj in json_node['projects']:
      prj_ref = first_true(profile.projects, None, lambda p: p.name == prj)
      check_always(prj_ref, 'Invalid project reference: %s' % prj)
      prj_ref.parent = self
      self.projects += [prj_ref]

  def serialize(self):
    return {
      'name': self.name,
      'period': str(self.period),
      'web': self.web,
      'role': self.role,
      'description': self.description,
      'notes': self.notes,
      'logo': self.logo,
      'projects': list(str(x) for x in self.projects)
    }
