from tex_printer import *
from utils import *

class EmploymentCardPrinter(SingleCardPrinter):
  def set_data(self, employment):
    self.employment = employment

  def print_employment(self, role, company, period, description, web, notes=[]):
    self.write([
      r' %s-' % to_month_year(period.startDate),
      '',
      r'%s' % to_month_year(period.endDate),
        r'\sffamily \textbf{%s}, ' % (role),
        r'\sffamily %s' % (company),
        r'',
        r'\rmfamily %s' % self.get_href(web),
        r'',
        r'\rmfamily %s' % latex_escape(description),
        r''
    ])

    for note in notes:
      self.write([r' %s' % note])

    self.write([
    ])

  def generate_content(self, employment):
    notes = []

    if employment.projects:
      prj_names = []
      for prj in employment.projects:
        prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]
      note = 'worked in %s project%s' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')
      notes += [note]

    notes += employment.notes

    self.print_employment(employment.role, employment.name, employment.period, employment.description, employment.web, notes)
