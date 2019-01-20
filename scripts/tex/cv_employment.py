from utils import *
from tex.elements import *


class EmploymentBlock:
  def __init__(self, tex_printer, employment):
    self.__printer = tex_printer
    self.__employment = employment
    self.print()

  def print(self):
    with MinipageElement(self.__printer, '30pt'):
      self.__printer.write([
        r'\includegraphics[width=30pt,height=30pt,keepaspectratio]{%s}' % (self.__printer.image_path(self.__employment.logo)),
      ])
  
    with MinipageElement(self.__printer, r'{\textwidth-30pt}'):
      start_date = to_month_year(self.__employment.period.startDate)
      end_date = 'Present' if self.__employment.period.isOpen else to_month_year(self.__employment.period.endDate)

      self.__printer.write([
        r'\itemhead{\textbf{%s}}' % (self.__employment.role),
        r'',
        r'\itemsubsubhead{\textbf{%s}}' % (self.__employment.name),
        r'',
        r'\itemsubsubhead{%s-%s}' % (start_date, end_date),
        r'',
      ])

    self.__printer.write([
      r'%s' % latex_escape(self.__employment.description),
      r'',
      r'%s' % self.__printer.get_href(self.__employment.web),
      r''
    ])
  
    notes = []

    if self.__employment.projects:
      prj_names = []
      for prj in self.__employment.projects:
        prj_names += ['\projectlink{%d}{%s}' % (prj.id, latex_escape(prj.name))]
      note = 'worked in %s project%s' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')
      notes += [note]

    notes += self.__employment.notes
  
    if notes:
      self.__printer.write([
        r'\begin{itemize-cv}'
      ])

      for note in notes:
        self.__printer.write([r'\item %s' % note])

      self.__printer.write([
        r'\end{itemize-cv}'
      ])
