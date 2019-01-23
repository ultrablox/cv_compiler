from utils import *


class ProjectElement:
  def __init__(self, tex_printer, project):
    self.__printer = tex_printer
    self.__project= project
    self.print()

  def print(self):
    
    place = 'hobby'
    if self.__project.parent:
      place = 'in \emplink{%d}{%s}' % (self.__project.parent.id, self.__project.parent.name)

    period = self.__project.get_period()
  
    skills = self.__project.get_total_skill_list()

    prj_link_id = 'prj_%d' % self.__project.id
    
    end_date = str(period.endDate.year) if not period.isOpen else 'present'
    self.__printer.write([
      r'\hypertarget{%s}{\itemhead{\textbf{%s}}}' % (prj_link_id, latex_escape(self.__project.name)),
      r'',
      r'\itemsubsubhead{\textbf{%d-%s, %s}}' % (period.startDate.year, end_date, place),
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
