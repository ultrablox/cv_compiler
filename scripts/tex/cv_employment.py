from utils import *


class EmploymentBlock:
  def __init__(self, tex_printer, employment):
    self.__printer = tex_printer
    self.__employment= employment
    self.print()

  def print(self):
    self.__printer.write([
      r'\itemhead{\textbf{%s}}' % (self.__employment.role),
      # r'',
      # r'\itemsubhead{\textbf{%s}}' % self.__employment.name,
      r'',
      r'\itemsubsubhead{\textbf{%s}, %s-%s}' % (self.__employment.name, to_month_year(self.__employment.period.startDate), to_month_year(self.__employment.period.endDate)),
      r'',
      r'%s' % latex_escape(self.__employment.description),
      r'',
      r'%s' % self.__printer.get_href(self.__employment.web),
      r''
    ])
  
    notes = []

    if self.__employment.projects:
      prj_names = []
      for prj in self.__employment.projects:
        prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]
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
