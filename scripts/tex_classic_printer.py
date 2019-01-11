from tex_printer import *


class TexSectionPrinter(TexPrinter):
  def print_data(self, profile):
    self.__begin()
    self.print_head()
    self.__middle()
    self.print_body(profile)
    self.__end()

  def print_head(self):
    self.write([r'\sectionhead{%s}' % self.HEADER])

  def __begin(self):
    self.write([r'\begin{paracol}{2}',
      r'\parbox[t]{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{'
    ])

  def __middle(self):
    self.write(['}',
      r'\switchcolumn'
    ])

  def __end(self):
    self.write([r'\end{paracol}',
      r'\vspace{\sectionspace}'])


class ContactsPrinter(TexSectionPrinter):
  HEADER = 'Personal and Contact Info'

  def print_body(self, profile):
    age = calculate_age(datetime.datetime.strptime(profile.personal['birthdate'], '%d.%m.%Y'))

    self.write([r'\sffamily \textbf{%s}, ' % profile.personal['name'],
      # r'\splitter',
      r'%s,' % profile.personal['sex'],
      r'%d y.o. (%s),' % (age, profile.personal['birthdate']),
      r'',
      r'{\rmfamily\color{gray} Residence: %s' % profile.contacts['residence'],
      r'\splitter',
      r'%s citizen}' % profile.personal['nationality'],
      r''
    ])
    head_line = 'Name: %s \splitter Sex: %s \splitter Date of birth: %s \splitter Nationality: %s' % (profile.personal['name'], profile.personal['sex'], profile.personal['birthdate'], profile.personal['nationality'])

    if profile.personal['additional']:
      head_line += '\splitter %s' % profile.personal['additional']
    head_line += '\hfill \\break'

    # self.writeln(head_line)
    # self.writeln('%s \hfill \\break' % profile.contacts['residence'])

    self.write([r'\rmfamily \vcenteredinclude{%s} \href{mailto:%s}{%s}' % (self.image_path('img/email.svg'), profile.contacts['email'], profile.contacts['email']),
      r'\vcenteredinclude{%s} %s' % (self.image_path('img/phone.svg'), profile.contacts['phone']),
      r'\vcenteredinclude{%s} %s' % (self.image_path('img/linkedin.svg'), self.get_href(profile.contacts['linkedin'], True)),
      r'\vcenteredinclude{%s} %s' % (self.image_path('img/skype.svg'), profile.contacts['skype']),
      r''
    ])

    self.write([r'\rmfamily %s' % ', '.join(profile.contacts['languages']),
      ''
    ])


class ProjectsPrinter(TexSectionPrinter):
  HEADER = 'Main Projects'

  def print_head(self):
    self.write([r'\sectionhead{%s}' % self.HEADER,
      r'\rmfamily\color{gray}\fontsize{9}{9}\selectfont most relevant first'
    ])

  def skills_line(self, prj):
    all_skills = prj.get_total_skill_list()
    if all_skills:
      return '\skills{%s}' % latex_escape(', '.join(all_skills))
    else:
      return ''

  def print_task(self, task):
    self.writeln(r'\item[\done] %s' % latex_escape(task.description))
    if task.achievements:
      self.writeln(r'\begin{itemize-achievments}')
      for ach in task.achievements:
        self.writeln(r'\item %s' % latex_escape(ach))
      self.writeln(r'\end{itemize-achievments}')
    else:
      self.writeln('')

  def print_tasks(self, tasks):
    self.writeln(r'\begin{itemize-cv}')
    for task in tasks:
      self.print_task(task)
    self.writeln(r'\end{itemize-cv}')

      # self.print_task(task)
  def print_project_data(self, name, period, description, skills, place, web, tasks):
    logo = 'img/education.svg'

    if place == 'hobby':
      logo = 'img/github_logo.svg'

    self.write([
      r'\begin{minipage}[t]{40pt}',
      r'\raggedleft',
      r'\regulartext %s-' % to_month_year(period.startDate),
      '',
      r'%s' % to_month_year(period.endDate),
      r'\end{minipage}',
      r'\hspace{2pt}',
      r'\begin{minipage}[t]{26pt}',
      r'\vspace{-8pt}'
      r'%s' % self.image(logo, 24),
      r'\end{minipage}',
      r'\hspace{2pt}',
      r'\begin{minipage}[t]{0.6\textwidth}',
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

    # for note in notes:
    #   self.write([r'\regulartext %s' % note])

    # Tasks
    self.print_tasks(tasks)

    self.write([
      r'\end{minipage}',
      r''
    ])

  def print_body(self, profile):
    sorted_projects = sorted(profile.projects, key=lambda prj: prj.get_period().startDate, reverse=True)
    for prj in sorted_projects:
      if prj.visible:
        place = 'in %s' % prj.parent.name if prj.parent else 'hobby'
        self.print_project_data(prj.name, prj.get_period(), prj.description, prj.get_total_skill_list(), place, prj.webLink, prj.tasks)
        self.writeln('\\vspace{\\blocksep}')


class EmploymentsPrinter(TexSectionPrinter):
  HEADER = 'Employment History'

  def print_employment(self, role, company, period, description, web, notes=[]):
    self.write([
      r'\begin{minipage}[t]{40pt}',
      r'\raggedleft',
      r'\regulartext %s-' % to_month_year(period.startDate),
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
      self.write([r'\regulartext %s' % note])

    self.write([
      r'\end{minipage}'
    ])

  def print_body(self, profile):
    for employment in profile.employments:
      notes = []

      if employment.projects:
        prj_names = []
        for prj in employment.projects:
          prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]
        note = 'worked in %s project%s' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')
        notes += [note]

      notes += employment.notes

      self.print_employment(employment.role, employment.name, employment.period, employment.description, employment.web, notes)
      self.write([
        '',
        r'\vspace{\blocksep}'
      ])


class EducationsPrinter(TexSectionPrinter):
  HEADER = 'Education'

  def print_facility_data(self, degree, facility, period, gpa, web = None, notes = []):
    self.write([
      r'\begin{minipage}[t]{40pt}',
      r'\raggedleft',
      r'\vspace{-8pt}'
      r'%s' % self.image('img/book.svg', 24),
      '',
      r'\regulartext %s-' % to_month_year(period.startDate),
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
      # self.write([r'\begin{itemize}'])
      for note in notes:
        self.write([r'\rmfamily %s' % note])
      # self.write([r'\end{itemize}'])

    self.write([
      r'\end{minipage}'
    ])

  def print_facility(self, facility):
    self.print_facility_data(facility['degree'],
        facility['facility'], 
        TimePeriod(facility['period']),
        facility['gpa'],
        facility['web'],
        facility['notes']
      )
    self.write(['\\vspace{\\blocksep}'])

  def print_body(self, profile):
    for edu in profile.education:
      self.print_facility(edu)


class ActivitiesPrinter(TexSectionPrinter):
  HEADER = 'Professional Activities'

  def print_body(self, profile):
    if not profile.has_activities():
      return

    # Scientific are most valuable
    if profile.scientificPubs:
      summary_str = '%d total' % len(profile.scientificPubs)
      if profile.scopus_publication_count():
        summary_str += ', incl. %d Scopus' % profile.scopus_publication_count()
      # self.write(['\t\\textbf{Recent Scientific Publications} (%s)' % summary_str,
        # '\t\\begin{itemize-noindent}'])
      self.write([r'\sffamily \textbf{Recent Scientific Publications}',
        r'',
        r'{\rmfamily \color{gray} %s}' % summary_str,
        r''])

      self.writeln(r'\begin{itemize-noindent}')
      for pub in profile.scientificPubs:
        if pub['visible']:
          is_scopus = '\scopus' if (('source' in pub) and (pub['source'] == 'Scopus')) else ''
          self.writeln(r'\item \rmfamily %d --- %s // %s %s' % (int(pub['year']), pub['title'], pub['journal'], is_scopus))

      self.writeln(r'\end{itemize-noindent}')

    # Popular publications are less important
    if profile.popularPubs:
      years = int(profile.popularPubs[0]['year']) - int(profile.popularPubs[-1]['year']) + 1
      summary_str = '%d total, avg. %.1f publicatons / year' % (len(profile.popularPubs), float(len(profile.popularPubs))/years)
      # self.write(['\t\\textbf{Recent Popular Publications} (%s):' % summary_str,
      #   '\\begin{itemize-noindent}'
      # ])
      self.write([r'\sffamily \textbf{Recent Popular Publications}',
        r'',
        r'{\rmfamily \color{gray} %s}' % summary_str,
        r''])

      self.writeln(r'\begin{itemize-noindent}')
      for pub in profile.popularPubs:
        if pub['visible']:
          self.writeln(r'\item \rmfamily \ppublication{%d}{%s}{%s}{%s}' % (int(pub['year']), pub['title'], pub['source'], pub['url']))
      self.writeln(r'\end{itemize-noindent}')

    # Conferences are the least important
    if profile.conferences:
      years = int(profile.conferences[0]['year']) - int(profile.conferences[-1]['year']) + 1
      summary_str = '%d total, avg. %.1f presentations / year' % (len(profile.conferences), float(len(profile.popularPubs))/years)
      conf_strs = []
      for conf in profile.conferences:
        conf_strs += ['%s (%s, %d)' % (conf['name'], conf['location'], conf['year'])]

      self.write([r'\sffamily \textbf{Conference Presentations}',
        r'',
        r'{\rmfamily \color{gray} %s}' % summary_str,
        r'',
        r'\rmfamily %s, etc.' % ' '.join(conf_strs),
        r''
      ])
      # self.writeln("\t\\textbf{Speaker of} (%s): %s, etc." % (summary_str, ' '.join(conf_strs)))


class LeadPrinter(TexSectionPrinter):
  HEADER = 'Objective and Summary'

  def print_body(self, profile):
    self.write([r'\regulartext %s' % profile.lead])


class TraitsPrinter(TexSectionPrinter):
  HEADER = 'Interests and Personal Traits'

  def print_body(self, profile):
    self.write([r'\regulartext',
      r'\begin{itemize-noindent}'])

    for trait in profile.traits:
      self.write([r'\item \textbf{%s:} %s' % (trait['name'], trait['details'])])

    self.write(['\\end{itemize-noindent}'])


class SkillsPrinter(TexSectionPrinter):
  HEADER = 'Professional Skills'

  def print_body(self, profile):
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

    # for sgr in profile.specialSkillGroups:
    #   self.write(['\skillgroup{%s:}{%s}{' % (sgr['name'], sgr['details'])])
    #   for adv in sgr['advantages']:
    #       self.write(['\item %s' % adv])
    #   self.write(['}'])


class TexClassicPrinter(TexPrinter):
  PAGE_PROFILES = {
    'a4' : {
      'margins' : [20, 15, 20, 10]
    },
    'a5' : {
      'margins' : [10, 7, 10, 5]
    }
  }

  def print_styles(self):
    self.write([
      '\\newcommand{\weblink}[2]{',
         '\\vcenteredinclude{%s} \href{#1}{#2}' % self.image_path('img/internet.svg'),
        '}',
      '\\newcommand{\\teamsize}[1]{',
        '\\vcenteredinclude{%s}  #1' % self.image_path('img/man.svg'),
      '}',
      '\\newcommand{\\codesize}[1]{',
        '\\vcenteredinclude{%s}  #1' % self.image_path('img/code.svg'),
      '}',
      '\\newcommand{\\achievement}[1]{',
        '\\vcenteredinclude{%s} #1' % self.image_path('img/star.svg', [8, 8]),
      '}',
      '\\newcommand{\skills}[1]{',
        '\\vcenteredinclude{%s} #1' % self.image_path('img/idea.svg'),
      '}'])

  def print_data(self, profile, file):
    page_profile = self.PAGE_PROFILES[self.paperSize]
    margins = page_profile['margins']
    self.write([
      '\documentclass[10pt]{ultracv}',
      '\\usepackage[%spaper, top=%dmm, bottom=%dmm, left=%dmm, right=%dmm]{geometry}' % (self.paperSize, margins[0], margins[1], margins[2], margins[3]),
      # '\\usepackage[a5paper, top=10mm, bottom=7mm, includehead, includefoot]{geometry}',
      r'\usepackage{fancyhdr,graphicx}',
      '' if self.paperSize == 'a5' else '\\pagestyle{fancy}',
      '\\fancyhf{}',
      r'\fancyhead[R]{\rmfamily %s}' % profile.personal['name'],
      '\\fancyhead[C]{\\thepage}'
    ])

    self.write([r'\graphicspath{{%s/}}' % os.path.abspath(os.path.join(self.rootDir, '.converted', 'repo', 'resources'))])

    self.image_path('img/correct.svg')

    if self.enableWatermark:
      self.write(['\\lhead{\setlength{\\unitlength}{1pt}',
        '\\begin{picture}(0,0)',
        '\put(-36,-10){\includegraphics[width=28pt]{%s}}' % self.image_path('watermark.svg'),
        '\end{picture}}'
      ])

    self.write([
      '\\renewcommand{\headrulewidth}{0.4pt}',
      # '\\renewcommand{\\footrulewidth}{0.4pt}',
      '\input{styles.tex}'
    ])

    self.print_styles()
    self.write([
      '\\begin{document}'
      ])

    printers = [ContactsPrinter, LeadPrinter, EducationsPrinter, SkillsPrinter, ProjectsPrinter, EmploymentsPrinter, ActivitiesPrinter, TraitsPrinter]
    # printers = [ProjectsPrinter]

    for printer in printers:
      printer(self.rootDir, self.rcPaths).print(profile, self.file)

    self.write(['\end{document}'])

