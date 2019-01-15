from tex_printer import *
from utils import *

class EmploymentCardPrinter(SingleCardPrinter):
  def set_data(self, employment):
    self.employment = employment

  def print_employment(self, role, company, period, description, web, notes=[]):
    SPACING = 2.75

    self.write([
      r'\begin{textblock}{44}[0, 0](%d,%d)' % (SPACING, SPACING),
      r'\includegraphics[width=\textwidth,keepaspectratio]{%s}' % (self.image_path('img/education.svg')),
      r'\end{textblock}'
    ])

    self.write([
      r'\begin{textblock}{%d}[0, 0](%d,%d)' % (self.width - 44 - 3*SPACING, SPACING + 44 + SPACING, SPACING),
      r'\cvhead{%s}' % role,
      r'',
      r'\cvsubhead{%s}' % company,
      r'',
      r'\cvsubsubhead{%s}' % self.get_href(web),
      r'',
      r'\rmfamily %s' % latex_escape(description),
      r'\end{textblock}'
    ])

    self.write([
      r'\begin{textblock}{44}[0, 0](%d,%d)' % (SPACING, SPACING + 44 + SPACING),
      r'\centering',
      r'{\rmfamily\fontsize{8}{8}\selectfont %s' % to_month_year(period.startDate),
      '',
      r'%s\par}' % to_month_year(period.endDate),
      r'\end{textblock}'
    ])


    self.write([
      r'\begin{textblock}{%d}[0, 0](%d,%d)' % (self.width - 2 * SPACING, SPACING, 70),
      r'\begin{itemize-cv}'
    ])

    for note in notes:
      self.write([r'\item %s' % note])

    self.write([
      r'\end{itemize-cv}',
      r'\end{textblock}'
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
