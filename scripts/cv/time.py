
import datetime

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

    assert self.startDate < self.endDate, 'Invalid time period : %s' % self

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
