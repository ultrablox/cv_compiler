
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
    return '%s-%s' % (self.startDate.strftime(TimePeriod.DATE_FORMAT), self.endDate.strftime(TimePeriod.DATE_FORMAT))


class DateIndexer:
  def __init__(self, min_date, max_date):
    self.minDate = min_date
    self.maxDate = max_date

  def month_count(self):
    return self.index(self.maxDate)

  def index(self, date):
    return (date.year - self.minDate.year) * 12 + (date.month - self.minDate.month)


class Task:
  def __init__(self, json_node):
    self.description = json_node['description']
    self.period = TimePeriod(json_node['period'])
    self.skills = json_node['skills']

    self.achievements = []
    if 'achievements' in json_node:
      self.achievements = json_node['achievements']


class Project:
  def __init__(self, prj_node):
    self.parent = None
    self.name = prj_node['name']
    self.linesOfCode = int(prj_node['code_size']) if 'code_size' in prj_node else None

    self.icon = ''
    if 'icon' in prj_node:
        self.icon = prj_node['icon']

    self.description = prj_node['description']
    if 'web' in prj_node:
        self.webLink = prj_node['web']
    else:
        self.webLink = None

    self.teamSize = prj_node['team-size']

    self.skills = []
    if 'skills' in prj_node:
        for skill in prj_node['skills']:
            self.skills += [skill]

    if 'secondary_skills' in prj_node:
        for skill in prj_node['secondary_skills']:
            self.skills += [skill['name']]        

    self.notes = []
    if 'notes' in prj_node:
        self.notes += [prj_node['notes']]

    self.tasks = []
    for task_node in prj_node['tasks']:
      self.tasks += [Task(task_node)]

    if 'period' in prj_node:
      self.period = TimePeriod(prj_node['period'])

    if 'hidden' in prj_node:
      self.visible = not prj_node['hidden']
    else:
      self.visible = True

  def get_total_skill_list(self):
    res = []
    res += self.skills
    for task in self.tasks:
      res += task.skills

    return sorted(set(res))

  def get_period(self):
    if self.tasks:
      res = copy.deepcopy(self.tasks[0].period)
      for i in range(1, len(self.tasks)):
        res.startDate = min(res.startDate, self.tasks[i].period.startDate)
        res.endDate = min(res.endDate, self.tasks[i].period.endDate)
      return res
    else:
      return self.period


class Skill:
  def __init__(self, short_name, json_node={}):
    log_print(LOG_LEVEL_DEBUG, 'Creating skill: %s' % short_name)
    self.name = short_name
    self.periods = []
    self.fullName = json_node['full_name'] if ('full_name' in json_node) else short_name
    if 'attitude' in json_node:
      switcher = {
          'favourite': SkillAttitude.FAVOURITE,
          'neutral': SkillAttitude.NEUTRAL,
          'negative': SkillAttitude.NEGATIVE
      }
      self.attitude = switcher.get(json_node['attitude'], lambda: None)
    else:
      self.attitude = SkillAttitude.NEUTRAL

  def name_with_abbr(self):
    if self.name == self.fullName:
      return self.name
    else:
      return '%s (%s)' % (self.fullName, self.name)

  def add_period(self, new_period):
    log_print(LOG_LEVEL_DEBUG, 'Adding period for %s: %s' % (self.name, new_period))
    self.periods += [new_period]

  def total_size(self):
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
  def __init__(self, json_node, profile):
    self.name = json_node['name']
    self.period = TimePeriod(json_node['period'])
    self.web = json_node['web']
    self.role = json_node['role']
    self.description = json_node['description']
    self.notes = json_node['notes'] if 'notes' in json_node else []
    self.logo = json_node['logo']

    self.projects = []
    for prj in json_node['projects']:
      prj_ref = first_true(profile.projects, None, lambda p: p.name == prj)
      assert prj_ref != None
      prj_ref.parent = self
      self.projects += [prj_ref]
