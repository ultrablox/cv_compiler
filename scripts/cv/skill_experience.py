import logging
from cv.time import *

class SkillAttitude:#(Enum)
    NEUTRAL = 0#auto()
    FAVOURITE = 1#auto()
    NEGATIVE = 2#auto()


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
    logging.debug('Adding period for %s: %s' % (self.skill.name, new_period))
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
