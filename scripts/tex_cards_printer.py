from tex_printer import *
from skill_matrix import *


class PlaceholderCardPrinter(TexPrinter):
  def print_data(self):
    self.write([
      r'placeholder data'
    ])

class PersonalCardPrinter(TexPrinter):
  def set_data(self, profile):
    self.profile = profile

  def print_data(self):
    age = calculate_age(datetime.datetime.strptime(self.profile.personal['birthdate'], '%d.%m.%Y'))

    self.write([
      r'\begin{minipage}[t]{64pt}',
      r'\vspace{-8pt}'
      r'%s' % self.image('img/education.svg', 62),
      r'\end{minipage}'
    ])

    self.write([
      r'\begin{minipage}[t]{100pt}',
      r'\sffamily \textbf{%s}' % self.profile.personal['name'],
      r'',
      r'{\rmfamily\color{gray}',
      r'%s,' % self.profile.personal['sex'],
      r'%d y.o. (%s)' % (age, self.profile.personal['birthdate']),
      r'}',
      r'',
      r'\rmfamily %s' % self.profile.contacts['residence'],
      r'',
      r'\rmfamily %s' % self.profile.personal['nationality'],
      r'\end{minipage}',
      r''
    ])

    self.write([r'\vspace{4pt}',
      r''
    ])

    self.write([
      r'\begin{minipage}[t]{64pt}',
      r'\raggedleft',
      r'\vcenteredinclude{%s}' % self.image_path('img/email.svg'),
      r'',
      r'\vcenteredinclude{%s}' % self.image_path('img/phone.svg'),
      r'',
      r'\vcenteredinclude{%s}' % self.image_path('img/linkedin.svg'),
      r'',
      r'\vcenteredinclude{%s}' % self.image_path('img/skype.svg'),
      r'',
      r'\end{minipage}'
    ])

    self.write([
      r'\begin{minipage}[t]{100pt}',
      r'\rmfamily \href{mailto:%s}{%s}' % (self.profile.contacts['email'], self.profile.contacts['email']),
      r'',
      r'\rmfamily %s' % (self.profile.contacts['phone']),
      r'',
      r'\rmfamily %s' % (self.get_href(self.profile.contacts['linkedin'], True)),
      r'',
      r'\rmfamily %s' % (self.profile.contacts['skype']),
      r''
      r'\end{minipage}',
      r''
    ])

    self.write([r'\vspace{4pt}',
      r''
    ])

    # Languages
    self.write([
      r'\begin{minipage}[t]{64pt}',
      r'\raggedleft'])

    for lang in self.profile.contacts['languages']:
      self.write([r'\rmfamily %s' % lang,
        ''])

    self.write([
      r'\end{minipage}'
    ])

    self.write([
      r'\begin{minipage}[t]{20pt}',
      r'\vcenteredinclude{%s}' % self.image_path('img/perfect.svg'),
      r'',
      r'\vcenteredinclude{%s}' % self.image_path('img/good.svg'),
      r'',
      r'\vcenteredinclude{%s}' % self.image_path('img/bad.svg'),
      r'',
      r'\end{minipage}',
      r''
    ])

    # self.write([r'\rmfamily %s' % ', '.join(),
    #   ''
    # ])

class EducationCardPrinter(TexPrinter):
  def set_data(self, profile):
    self.profile = profile

  def print_facility_data(self, degree, facility, period, gpa, web = None, notes = []):
    self.write([
      r'\begin{minipage}[t]{40pt}',
      r'\raggedleft',
      r'\vspace{-8pt}'
      r'%s' % self.image('img/book.svg', 24),
      '',
      r' %s-' % to_month_year(period.startDate),
      '',
      r'%s' % to_month_year(period.endDate),
      r'\end{minipage}',
      r'\hspace{6pt}',
      r'\begin{minipage}[t]{0.8\textwidth}',
        r'\sffamily \textbf{%s}, ' % (degree),
        # r'',
        r'\sffamily %s' % (facility),
        r'',
        r'\rmfamily %s' % self.get_href(web),
        r'',
        r'\rmfamily %s' % latex_escape(gpa),
        r''
    ])

    if notes:
      for note in notes:
        self.write([r'\rmfamily %s' % note])

    self.write([
      r'\end{minipage}'
    ])

  def print_data(self):
    for facility in self.profile.education:
      self.print_facility_data(facility['degree'],
        facility['facility'], 
        TimePeriod(facility['period']),
        facility['gpa'],
        facility['web'],
        facility['notes']
      )

class SkillsCardPrinter(TexPrinter):
  def set_data(self, profile):
    self.profile = profile

  def print_data(self):
    profile = self.profile
    skill_matrix = SkillMatrix(profile)
    skill_matrix.generate(self.file)

    totals = profile.skills_totals()
    totals = totals[VISUAL_SKILL_COUNT:]

    skill_groups = {}
    #0, <1yr, 1-2yr, 2-5, 5-7, 7-10, 10+
    barriers = [0, 1, 2, 5, 7, 10, 1000]
    cur_gr_idx = 0

    for skill in totals:
      gr_val = 0
      for idx in range(0, len(barriers)):
        if (barriers[idx] <= skill['size']) and (skill['size'] < barriers[idx+1]):
            gr_val = barriers[idx]
            break

      if gr_val in skill_groups:
          skill_groups[gr_val] += [skill]
      else:
          skill_groups[gr_val] = [skill]

    first_non_empty = True
    for barrier in reversed(barriers):
      if barrier in skill_groups:
        barrier_idx = barriers.index(barrier)

        skills = []
        max_size = 0
        for sk in skill_groups[barrier]:
            skills += [latex_escape(sk['name'])]
            max_size = max(max_size, sk['size'])

        max_val_name = str(barriers[barrier_idx+1])
        if first_non_empty:
            max_val_name = '%.1f' % max_size
            first_non_empty = False

        group_name = '<%s year' % max_val_name if barrier_idx == 0 else '%d-%s years' % (barriers[barrier_idx], max_val_name)

        self.writeln(r'\rmfamily \textbf{%s:} %s \newline' % (group_name, ', '.join(skills)))


class ProjectCardPrinter(TexPrinter):
  def set_data(self, project):
    self.project = project

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
    logo = 'img/education.svg'

    if place == 'hobby':
      logo = 'img/github_logo.svg'

    self.write([
      r' %s-' % to_month_year(period.startDate),
      '',
      r'%s' % to_month_year(period.endDate),
        r'\sffamily \textbf{%s}, ' % latex_escape(name),
        r'%s' % place,
        r'',
        r'\rmfamily %s' % latex_escape(description),
        r'',
        r'\rmfamily \textit{%s}' % latex_escape(', '.join(skills)),
        r'',
        r'\rmfamily %s' % self.get_href(web),
        r''
    ])

    self.writeln(r'\begin{itemize-cv}')
    for task in tasks:
      self.print_task(task)
    self.writeln(r'\end{itemize-cv}')

    self.write([
      r''
    ])

  def print_data(self):
    # sorted_projects = sorted(self.projects, key=lambda prj: prj.get_period().startDate, reverse=True)
    # for prj in sorted_projects:

      prj = self.project
      place = 'in %s' % prj.parent.name if prj.parent else 'hobby'
      self.print_project_data(prj.name, prj.get_period(), prj.description, prj.get_total_skill_list(), place, prj.webLink, prj.tasks)
      # self.writeln('\\vspace{\\blocksep}')


class EmploymentCardPrinter(TexPrinter):
  def set_data(self, employment):
    self.employment = employment

  def print_employment(self, role, company, period, description, web, notes=[]):
    self.write([
      r'\begin{minipage}[t]{40pt}',
      r'\raggedleft',
      r' %s-' % to_month_year(period.startDate),
      '',
      r'%s' % to_month_year(period.endDate),
      r'\end{minipage}',
      r'\hspace{2pt}',
      r'\begin{minipage}[t]{26pt}',
      r'\vspace{-8pt}'
      r'%s' % self.image('img/education.svg', 24),
      r'\end{minipage}',
      r'\hspace{2pt}',
      r'\begin{minipage}[t]{0.6\textwidth}',
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
      r'\end{minipage}'
    ])

  def print_data(self):
    employment = self.employment

    notes = []

    if employment.projects:
      prj_names = []
      for prj in employment.projects:
        prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]
      note = 'worked in %s project%s' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')
      notes += [note]

    notes += employment.notes

    self.print_employment(employment.role, employment.name, employment.period, employment.description, employment.web, notes)
    # self.write([
    #   '',
    #   r'\vspace{\blocksep}'
    # ])

class TexCardsPrinter(TexPrinter):
  CARD_WIDTH = 170
  CARD_HEIGHT = 168
  CARDS_IN_ROW = 3
  HEADER_HEIGHT = 24
  HOR_SPACING = 4
  def print_header_row(self, headers):
    for header in headers:
      self.write([
          # r'\fbox{',
          r'\begin{minipage}[t][%dpt]{%dpt}' % (self.HEADER_HEIGHT, self.CARD_WIDTH)
        ])

      heading = header['header']
      if heading:
        self.write([
          r'\vspace{0pt}',
          r'\sffamily\textbf{%s}' % heading,
          r'',
          r'\rmfamily\color{gray} less relevant info'
        ])
      else:
        self.write([
          r'\vspace{0pt}',
          r'\vphantom{\sffamily\textbf{X}}',
          r'\hfill'
          # r'\linebreak[0]'
        ])

      self.write([
        r'\end{minipage}',
        r'\hspace{%dpt}' % (self.HOR_SPACING - 1)
      ])  


  def print_data_row(self, cards):
    for card in cards:
      self.write([
        r'\begin{minipage}[t][%dpt]{%dpt}' % (self.CARD_HEIGHT, self.CARD_WIDTH),
        r'\fbox{'
      ])

      self.write([
        r'\begin{minipage}[t][%dpt]{%dpt}' % (self.CARD_HEIGHT - 4, self.CARD_WIDTH - 2),
        r'\vspace{6pt}'
      ])
        # r'\parbox{%dpt}{' % (self.CARD_WIDTH - 4),


      card['data'].print_data()

      self.write([
        r'\end{minipage}'
      ])

      self.write([
        r'}',
        r'\end{minipage}'
        r'\hspace{%dpt}' % self.HOR_SPACING
      ]) 


  def print_data_chain(self, data = []):
    for i in range(0, len(data), 3):
      self.print_header_row(data[i:i+3])
      self.write([
          r'',
        ])
      self.print_data_row(data[i:i+3])
      self.write([
          r'',
        ])


  def print_data(self, profile, file):
    self.write([
      r'\documentclass[10pt]{ucv-cards}',

      r'\usepackage[a4paper, top=10mm, bottom=10mm, left=10mm, right=10mm]{geometry}',
      r'\usepackage{fancyhdr,graphicx}',
      r'\pagestyle{fancy}',
      r'\fancyhf{}',
      # r'\fancyhead[R]{\rmfamily %s}' % profile.personal['name'],
      r'\fancyhead[C]{\thepage}',
      r'\setlength{\fboxsep}{0pt}',
    ])

    self.write([r'\graphicspath{{%s/}}' % os.path.abspath(os.path.join(self.rootDir, '.converted', 'repo', 'resources'))])

    self.image_path('img/correct.svg')

    self.write([
      r'\begin{document}',
      r'\setlength\parindent{0pt}'
      ])

    head_item = {
      'header' : 'Rare header',
      'data' : PlaceholderCardPrinter(self.rootDir, self.rcPaths, self.file)
    }

    empty_item = {
      'header' : '',
      'data' : PlaceholderCardPrinter(self.rootDir, self.rcPaths, self.file)
    }

    data = []

    # Personal and contacts
    pers_printer = PersonalCardPrinter(self.rootDir, self.rcPaths, self.file)
    pers_printer.set_data(profile)
    data += [{
      'header' : 'Personal and Contacts',
      'data' : pers_printer
    }]

    # Education
    edu_printer = EducationCardPrinter(self.rootDir, self.rcPaths, self.file)
    edu_printer.set_data(profile)

    data += [{
      'header' : 'Education',
      'data' : edu_printer
    }]

    # Skills
    skills_printer = SkillsCardPrinter(self.rootDir, self.rcPaths, self.file)
    skills_printer.set_data(profile)

    data += [{
      'header' : 'Professional skills',
      'data' : skills_printer
    }]

    # Projects
    projects_data = []
    for project in profile.projects:
      proj_printer = ProjectCardPrinter(self.rootDir, self.rcPaths, self.file)
      proj_printer.set_data(project)

      projects_data += [{
        'header' : '',
        'data' : proj_printer
      }]

    projects_data[0]['header'] = 'Main Projects'
    data += projects_data

    # Employment history
    employments_data = []
    for employment in profile.employments:
      emp_printer = EmploymentCardPrinter(self.rootDir, self.rcPaths, self.file)
      emp_printer.set_data(employment)

      employments_data += [{
        'header' : '',
        'data' : emp_printer
      }]
    employments_data[0]['header'] = 'Employment History'
    data += employments_data

    # Activities
    # data += [{
    #   'header' : 'Professional Activities',
    #   'data' : PlaceholderCardPrinter(self.rootDir, self.rcPaths, self.file)
    # }]

    # data += [empty_item]*20
    # for i in [0, 5, 7, 12]:
    #   data[i] = head_item

    self.print_data_chain(data)

    self.write(['\end{document}'])

