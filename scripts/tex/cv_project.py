from utils import *


class ProjectElement:
  def __init__(self, tex_printer, project):
    self.__printer = tex_printer
    self.__project= project
    self.print()

  def print(self):
    place = 'in %s' % self.__project.parent.name if self.__project.parent else 'hobby'
    period = self.__project.get_period()
  
    skills = self.__project.get_total_skill_list()

    self.__printer.write([
      r'\itemhead{\textbf{%s}}' % (latex_escape(self.__project.name)),
      r'',
      r'\itemsubsubhead{\textbf{%d-%d, %s}}' % (period.startDate.year, period.endDate.year, place),
      r'',
      r'\itemsubhead{%s}' % latex_escape(self.__project.description),
      r'',
      r'\skills{%s}' % latex_escape(', '.join(skills)),
      r'',
      r'%s' % self.__printer.get_href(self.__project.webLink),
      r''
    ])

    self.__printer.writeln(r'\begin{itemize-tasks}')
    for task in self.__project.tasks:
      self.__printer.writeln(r'\item %s' % latex_escape(task.description))
      if task.achievements:
        self.__printer.writeln(r'\begin{itemize-achievments}')
        for ach in task.achievements:
          self.__printer.writeln(r'\item %s' % latex_escape(ach))
        self.__printer.writeln(r'\end{itemize-achievments}')
      else:
        self.__printer.writeln('')
    self.__printer.write([
      r'\end{itemize-tasks}',
      r''
    ])
