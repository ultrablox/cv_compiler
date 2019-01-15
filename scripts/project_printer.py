from tex_printer import *
from utils import *


class ProjectCardPrinter(SingleCardPrinter):
  def print_task(self, task):
    self.writeln(r'\item[\done] %s' % latex_escape(task.description))
    if task.achievements:
      self.writeln(r'\begin{itemize-achievments}')
      for ach in task.achievements:
        self.writeln(r'\item %s' % latex_escape(ach))
      self.writeln(r'\end{itemize-achievments}')
    else:
      self.writeln('')

  def print_project_data(self, name, period, description, skills, place, web, tasks):
    self.write([
      r'\begin{textblock}{30}[0, 0](5,5)',
      r'\includegraphics[width=30pt,height=30pt,keepaspectratio]{%s}' % (self.image_path('img/education.svg')),
      r'\end{textblock}'
    ])

    self.write([
        r'\begin{textblock}{70}[1.0, 0](100,20)',
        r'xxx',
        r'\end{textblock}']
    )

    # logo = 'img/education.svg'

    # if place == 'hobby':
    #   logo = 'img/github_logo.svg'

    # self.write([
    #   r' %s-' % to_month_year(period.startDate),
    #   '',
    #   r'%s' % to_month_year(period.endDate),
    #     r'\sffamily \textbf{%s}, ' % latex_escape(name),
    #     r'%s' % place,
    #     r'',
    #     r'\rmfamily %s' % latex_escape(description),
    #     r'',
    #     r'\rmfamily \textit{%s}' % latex_escape(', '.join(skills)),
    #     r'',
    #     r'\rmfamily %s' % self.get_href(web),
    #     r''
    # ])

    # self.writeln(r'\begin{itemize-cv}')
    # for task in tasks:
    #   self.print_task(task)
    # self.writeln(r'\end{itemize-cv}')

    # self.write([
    #   r''
    # ])

  def generate_content(self, prj):
    place = 'in %s' % prj.parent.name if prj.parent else 'hobby'
    self.print_project_data(prj.name, prj.get_period(), prj.description, prj.get_total_skill_list(), place, prj.webLink, prj.tasks)
