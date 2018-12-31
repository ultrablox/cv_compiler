
from skill_attitude import *
from utils import *
import datetime


class TimePeriod:
  def __init__(self, data):
    interval = data.split('-')
    self.startDate = datetime.datetime.strptime(interval[0], '%d.%m.%Y')

    if interval[1] == 'now':
      self.endDate = datetime.datetime.now()
      self.isOpen = True
    else:
      self.endDate = datetime.datetime.strptime(interval[1], '%d.%m.%Y')
      self.isOpen = False

class DateIndexer:
    def __init__(self, min_date, max_date):
        self.minDate = min_date
        self.maxDate = max_date
    
    def month_count(self):
        return self.index(self.maxDate)

    def index(self, date):
        return (date.year - self.minDate.year) * 12 + (date.month - self.minDate.month)


class Project:
    def __init__(self, prj_node):
        self.parent = None
        
        self.period = TimePeriod(prj_node['period'])
        self.name = prj_node['name']

        self.icon = ''
        if 'icon' in prj_node:
            self.icon = prj_node['icon']

        self.description = prj_node['description']
        if 'web' in prj_node:
            self.webLink = prj_node['web']
        else:
            self.webLink = None

        self.teamSize = prj_node['team-size']

        self.achievements = []
        if 'achievements' in prj_node:
            self.achievements = prj_node['achievements']

        self.skills = []
        
        if 'skills' in prj_node:
            for skill in prj_node['skills']:
                self.skills += [skill]

        if 'secondary_skills' in prj_node:
            for skill in prj_node['secondary_skills']:
                self.skills += [skill['name']]        

        self.notes =[]
        if 'notes' in prj_node:
            self.notes += [prj_node['notes']]


class Skill:
    def __init__(self, name):
        self.name = name
        self.attitude = SkillAttitude.NEUTRAL
        self.totalExperience = 0
        self.periods = []

    def add_period(self, new_period):
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

            return sum(1 for item in months if item==(1)) / 12.0

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
