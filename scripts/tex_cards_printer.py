from tex_printer import *
from skill_matrix import *
from project_printer import *
from employment_printer import *

PT_IN_MM = 2.83465

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
      '',
      r' %s-' % to_month_year(period.startDate),
      '',
      r'%s' % to_month_year(period.endDate),
        r'\sffamily \textbf{%s}, ' % (degree),
        # r'',
        r'\sffamily %s' % (facility),
        r'',
        r'\rmfamily %s' % self.get_href(web),
        r'',
        r'\rmfamily %s' % latex_escape(gpa),
        r''
    ])

    # if notes:
    #   for note in notes:
    #     self.write([r'\rmfamily %s' % note])

    self.write([
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
    skill_matrix.generate(self.file, TexCardsPrinter.CARD_HEIGHT - 60)

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




# A4 =  210 mm x  297 mm =  595 pt x  842 pt
class TexCardsPrinter(TexPrinter):
  V_SPACING = 15
  CARD_WIDTH = (595 - 4 * V_SPACING)/3
  CARD_HEIGHT = 206
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


  def print_data_chain_good(self, data = []):
    for i in range(0, len(data), 3):
      self.print_header_row(data[i:i+3])
      self.write([
          r'',
        ])
      self.print_data_row(data[i:i+3])
      self.write([
          r'',
        ])

  def print_data_chain(self, data):
    for el in data:
      self.write([
         r'\fbox{'
        r'\begin{minipage}[t]{%dpt}' % (self.CARD_WIDTH),

      ])
      el['data'].print_data()
      self.write([

        r'\end{minipage}',
        r'}',
      #   # r'\hspace{%dpt}' % self.HOR_SPACING,
        r''
      ]) 

  def print_facility_data(self, degree, facility, period, gpa, web = None, notes = []):
    self.write([
      r'{\rmfamily\fontsize{12}{12}\selectfont %d - \textbf{%s}\par}' % (period.endDate.year, degree),
      '',
      # r' %s-' % to_month_year(period.startDate),
      # '',
      # r'%s' % to_month_year(period.endDate),
      #   r'\sffamily \textbf{%s}, ' % (degree),
      #   # r'',
        r'%s' % (facility),
        r'',
        r'%s' % self.get_href(web),
        r'',
        r'%s' % latex_escape(gpa),
        r'',
        r'\vspace{6pt}'
    ])

  def print_education(self, educations):
    for facility in educations:
      self.print_facility_data(facility['degree'],
        facility['facility'], 
        TimePeriod(facility['period']),
        facility['gpa'],
        facility['web'],
        facility['notes']
      )


  def print_skill_list(self, skills):

    skill_groups = {}
    #0, <1yr, 1-2yr, 2-5, 5-7, 7-10, 10+
    barriers = [0, 1, 2, 5, 7, 10, 1000]
    cur_gr_idx = 0

    for skill in skills:
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

        self.writeln(r'\cvnormal \textbf{%s:} %s \newline' % (group_name, ', '.join(skills)))


  def print_skill_chart(self, skills):
    skills.reverse()
    max_value = skills[0]['size']
    visual_count = len(skills)

    coords = ['{%s}' % x['name'] for x in skills]

    self.write(['\pgfplotsset{',
      'compat=1.13,',
      # 'every non boxed x axis/.append style={x axis line style=-},',
      # 'every non boxed y axis/.append style={y axis line style=-},',
      r'tick label style = {font=\cvnormal},',
      r'every axis label = {font=\cvnormal},',
      r'legend style = {font=\cvnormal},',
      r'label style = {font=\cvnormal},',
      r'}'
    ])

    self.write([r'\begin{tikzpicture}',
      r'\begin{axis}[',
      r'font=\cvnormal,',
      r'xlabel={Experience, years},',
      r'xbar stacked,',
      r'width=0.9\columnwidth,',
      # r'legend style={',
      # r'legend columns=4,',
      # r'    at={(xticklabel cs:0.5)},',
      # r'    anchor=north,',
      # r'    draw=none',
      # r'},',
      r'xtick=\empty,',
      r'ytick=data,',
      r'axis y line*=none,',
      # r'axis x line*=none,',
      r'axis x line*=top,',
      # r'x axis line style={-stealth},'
      # r'tick label style={font=\footnotesize},',
      # r'legend style={font=\footnotesize},',
      # r'label style={font=\footnotesize},',
      # r'xtick={0,100,...,600},',
      # r'bar width=6mm,',
      r'bar width=10pt,',
      r'yticklabels={%s},' % ','.join(coords),
      r'xmin=0,',
      # r'xmax=600,',
      r'area legend,',
      r'clip=false,',
      r'height=200pt,',
      # r'y=8mm,',
      # r'enlarge y limits={abs=0.625},',
      r'nodes near coords,',
      r'every node near coord/.append style={at ={(\pgfplotspointmeta,\pgfplotspointy)},anchor=west},',
      r'every node near coord/.append style={/pgf/number format/.cd, fixed, fixed zerofill, precision=1},',
      r'every node near coord/.append style={/pgf/number format/assume math mode=false},',
      r'visualization depends on=y \as \pgfplotspointy,',
      r'every axis plot/.append style={fill}',
      ']'])

    labels = ['Desired', 'Job\'s a job', 'Prefferably avoid']
    colors = ['green', 'gray', 'orange']

    vals = [[0] * visual_count, [0] * visual_count, [0] * visual_count]

    switcher = {
        SkillAttitude.FAVOURITE: 0,
        SkillAttitude.NEUTRAL: 1,
        SkillAttitude.NEGATIVE: 2
    }

    for i in range(0, visual_count):
      cur_skill = skills[i]
      att = cur_skill['attitude']
      idx = switcher.get(att, 0)
      vals[idx][i] = cur_skill['size']

    for i in range(0, 3):
      x_coords = [''] * visual_count
      for j in range(0, visual_count):
        x_coords[j] = '(%f,%d)' % (vals[i][j], j)
      format_str = ', nodes near coords*' if (i == 2) else ''

      self.write([
        r'\addplot[fill=%s%s, draw=none] coordinates {%s};' % (colors[i], format_str, latex_escape(' '.join(x_coords))),
      ])

      if i == 0:
        self.write([
          # r'\addlegendentry{%s}' % labels[i]
        ])
    # self.write([
    #   r'\addplot[green] coordinates',
    #   r'{(400,0) (0,1) (0,2) (0,3) (0,4) (0,5)};'
    # ])

    self.write([
      r'\end{axis}',
      r'\end{tikzpicture}',
      r'\newline'
    ])

  def print_skills(self, skills):
    VISUAL_SKILL_COUNT = 12
    self.print_skill_chart(skills[:VISUAL_SKILL_COUNT])
    self.print_skill_list(skills[VISUAL_SKILL_COUNT:])

  
  def print_employment(self, employment):
    self.write([
      r'\cvhead{%s}' % employment.role,
      r'',
      r'\cvsubhead{%s}' % employment.name,
      r'',
      r'\cvsubsubhead{%s}' % self.get_href(employment.web),
      r'',
      r'\rmfamily %s' % latex_escape(employment.description),
      r''
    ])
    
    self.write([
      r'{\rmfamily\fontsize{8}{8}\selectfont %s' % to_month_year(employment.period.startDate),
      r'%s\par}' % to_month_year(employment.period.endDate),
      ''
    ])

    if employment.notes:
      self.write([
        r'\begin{itemize-cv}'
      ])

      for note in employment.notes:
        self.write([r'\item %s' % note])

      self.write([
        r'\end{itemize-cv}',
        r''
      ])

  
  def print_project(self, project):
    place = 'in %s' % project.parent.name if project.parent else 'hobby'
    period = project.get_period()

    self.write([
      r'\cvsubhead{%s}' % (latex_escape(project.name)),
      r'',
      r'\cvsubsubhead{%d-%d}' % (period.startDate.year, period.endDate.year),
      r'',
      r'\cvirrelevant{%s}' % self.get_href(project.webLink),
      # r'\raggedleft',
      # r'\cvirrelevant{%s}' % (to_month_year(period.startDate), to_month_year(period.endDate), place),
      r'',
      r'\rmfamily %s' % latex_escape(project.description),
      r'',
      r'\rmfamily \textit{%s}' % latex_escape(', '.join(project.get_total_skill_list())),
      
      r''
    ])

    # for note in notes:
    #   self.write([r'\regulartext %s' % note])

    # Tasks
    # self.print_tasks(tasks)
    self.writeln(r'\begin{itemize-cv}')
    for task in project.tasks:
      self.writeln(r'\item[\done] %s' % latex_escape(task.description))
      if task.achievements:
        self.writeln(r'\begin{itemize-achievments}')
        for ach in task.achievements:
          self.writeln(r'\item %s' % latex_escape(ach))
        self.writeln(r'\end{itemize-achievments}')
      else:
        self.writeln('')
    self.writeln(r'\end{itemize-cv}')


    self.write([
      r''
    ])

  def print_personal(self, profile):
    age = calculate_age(datetime.datetime.strptime(profile.personal['birthdate'], '%d.%m.%Y'))

    self.write([
      r'\begin{minipage}{0.3\columnwidth}',
      r'\fbox{\includegraphics[width=0.9\textwidth,keepaspectratio]{%s}}' % self.image_path('img/photo.jpg', [62,62]),
      r'\end{minipage}',
      r'\begin{minipage}{0.67\columnwidth}',
      r'\cvhead{%s}' % profile.personal['name'],
      r'',
      r'\cvsubhead{%s, %s y.o.}' % (profile.personal['sex'], age),
      r'',
      r'\cvsubsubhead{Citizenship: %s}' % profile.personal['nationality'],
      r'',
      r'\cvsubsubhead{Residence: %s}' % profile.contacts['residence'],
      r'',
      r'\end{minipage}',
      r'',
      r'\colsectionspace'
    ])
    

  def print_contacts(self, profile):
    self.write([
      r'\noindent\rule{\columnwidth}{0.5pt}',
      r''
    ])

    linkedin_name = profile.contacts['linkedin'].split('/')[-1]

    self.write([
      r'\begin{minipage}{0.38\columnwidth}',
      r'\vcenteredinclude{%s}' % self.image_path('img/linkedin.svg'),
      r'\rmfamily %s' % linkedin_name,
      r'',
      r'\vcenteredinclude{%s}' % self.image_path('img/skype.svg'),
      r'\rmfamily %s' % (profile.contacts['skype']),
      r'\end{minipage}',
    ])

    self.write([
      r'\begin{minipage}{0.58\columnwidth}',
      r'\raggedleft',
      r'\rmfamily \href{mailto:%s}{%s}' % (profile.contacts['email'], profile.contacts['email']),
      r'\vcenteredinclude{%s}' % self.image_path('img/email.svg'),
      r'',
      r'\rmfamily %s' % (profile.contacts['phone']),
      r'\vcenteredinclude{%s}' % self.image_path('img/phone.svg'),
      r'\end{minipage}',
      r''
    ])
    self.write([
      r'',
      r'\noindent\rule{\columnwidth}{0.5pt}',
      r'',
      r'\colsectionspace',
      r''
    ])


  def print_head_column(self, profile):
    # Personal
    self.print_personal(profile)
    self.print_contacts(profile)

    # Objective
    self.write([
      r'\cvhead{About me}'
    ])

    self.write([  
      r'\cvnormal %s' % profile.lead,
      r'',
      r'\colsectionspace'
    ])

    # Education
    self.write([
      r'\cvhead{Education}',
      r''
    ])
    self.print_education(profile.education)
    self.write([  
      r'\colsectionspace',
      r''
    ])

    # Skills
    self.write([
      r'\cvhead{Skills}',
      r''
    ])
    self.print_skills(profile.skills_totals())


  def print_data(self, profile, file):
    EMPLOYMENT_CARD_HEIGHT = 100
    #
    # Print independent cards
    #

    # Employment history
    emp_files = []
    emp_printer = EmploymentCardPrinter(self.CARD_WIDTH, EMPLOYMENT_CARD_HEIGHT)
    emp_printer.init_resources(self.rcPaths, self.rootDir)
    for employment in profile.employments:
      out_pdf = os.path.join(self.rootDir, 'emp_%d.pdf' % employment.id)
      # emp_printer.compile_to(employment, out_pdf)
      emp_files += [out_pdf]

    # # Projects
    # prj_printer = ProjectCardPrinter(self.CARD_WIDTH, self.CARD_HEIGHT)
    # prj_printer.init_resources(self.rcPaths, self.rootDir)
    # for project in profile.projects:
    #   prj_printer.compile_to(project, os.path.join(out_dir, 'prj_%d.pdf' % project.id))


    out_dir = self.rootDir
    self.write([
      r'\documentclass[10pt]{ucv-cards}',
      r'\usepackage[a4paper, top=10mm, bottom=10mm, left=10mm, right=10mm]{geometry}',
    #   r'\usepackage{fancyhdr,graphicx}',
    #   r'\pagestyle{fancy}',
    #   r'\fancyhf{}',
    #   # r'\fancyhead[R]{\rmfamily %s}' % profile.personal['name'],
    #   r'\fancyhead[C]{\thepage}',
    #   r'\setlength{\fboxsep}{0pt}',
    ])

    # self.write([r'\graphicspath{{%s/}}' % os.path.abspath(os.path.join(self.rootDir, '.converted', 'repo', 'resources'))])

    # self.image_path('img/correct.svg')

    self.write([
      r'\begin{document}',
    #   r'\setlength\parindent{0pt}'
      ])

    # head_item = {
    #   'header' : 'Rare header',
    #   'data' : PlaceholderCardPrinter(self.rootDir, self.rcPaths, self.file)
    # }

    # empty_item = {
    #   'header' : '',
    #   'data' : PlaceholderCardPrinter(self.rootDir, self.rcPaths, self.file)
    # }

    # data = []

    # # Personal and contacts
    # pers_printer = PersonalCardPrinter(self.rootDir, self.rcPaths, self.file)
    # pers_printer.set_data(profile)
    # data += [{
    #   'header' : 'Personal and Contacts',
    #   'data' : pers_printer
    # }]

    # # Education
    # edu_printer = EducationCardPrinter(self.rootDir, self.rcPaths, self.file)
    # edu_printer.set_data(profile)

    # data += [{
    #   'header' : 'Education',
    #   'data' : edu_printer
    # }]

    # Skills
    # skills_printer = SkillsCardPrinter(self.rootDir, self.rcPaths, self.file)
    # skills_printer.set_data(profile)

    # data += [{
    #   'header' : 'Professional skills',
    #   'data' : skills_printer
    # }]






    #   emp_printer = EmploymentCardPrinter(self.rootDir, self.rcPaths, self.file)
    #   emp_printer.set_data(employment)

    #   employments_data += [{
    #     'header' : '',
    #     'data' : emp_printer
    #   }]
    # employments_data[0]['header'] = 'Employment History'
    # data += employments_data
    # exit(1)

    #   proj_printer = ProjectCardPrinter(self.rootDir, self.rcPaths, self.file)
    #   proj_printer.set_data(project)

    #   projects_data += [{
    #     'header' : '',
    #     'data' : proj_printer
    #   }]

    # projects_data[0]['header'] = 'Main Projects'
    # data += projects_data

    # Activities
    # data += [{
    #   'header' : 'Professional Activities',
    #   'data' : PlaceholderCardPrinter(self.rootDir, self.rcPaths, self.file)
    # }]
    self.write([
      r'\setlength{\parindent}{0pt}',
      r'\setlength{\columnsep}{4pt}',
      r'\setlength{\intextsep}{0pt}',
      # r'\columnratio{0.33}',
      # r'\begin{paracol}{2}'
      # r'\begin{wrapfigure}{l}{180pt}',
      # r'\begin{minipage}[t][0.98\textheight]{180pt}'
    ])
    
    self.write([
      r'\begin{textblock}{%d}[0, 0](%f,%f)' % (self.CARD_WIDTH, PT_IN_MM*10, PT_IN_MM*10),
    ])

    self.print_head_column(profile)

    self.write([
      r'\end{textblock}'
    ])

    self.write([
      # r'\end{minipage}',
      # r'\end{wrapfigure}'
      # r'\switchcolumn'
    ])
    
    self.write([
      '\clearpage',
    ])

    # self.write([
    #   r'\begin{minipage}[b][0.33\textheight]{400pt}',
    #   r'xxx',
    #   r'',
    #   r'xxx',
    #   r'',
    #   r'xxx',
    #   r'',
    #   r'xxx',
    #   r'',
    #   r'xxx',
    #   r'',
    #   r'xxx',
    #   r'\end{minipage}',
    #   # r'\end{wrapfigure}'
    #   # r'\switchcolumn'
    # ])
    
  
    

    # self.write([
    #   r'\cvhead{Main Projects}',
    #   r'',
    #   r'\cvsubsubhead{Relevant are first}',
    #   r''
    # ])
    
    


    self.write([
      # r'\begin{minipage}{0.67\textwidth}',
      # r'\fbox{'
      r'\newgeometry{top=10mm, bottom=10mm, left=%dpt, right=10mm}' % (self.CARD_WIDTH + 10*PT_IN_MM)
    ])

    for i in range(0, len(profile.projects), 2):
      projects = profile.projects[i:i+2]
  
    # for project in profile.projects:
      
      self.write([
        r'\setcolumnwidth{%fpt,%fpt}' % (self.CARD_WIDTH, self.CARD_WIDTH),
        r'\begin{paracol}{2}'
      ])

      if i == 0:
        self.write([
          r'[',
          r'\cvhead{Main Projects}',
          r'',
          r'\cvsubsubhead{Relevant are first}',
          r']'
        ])

      for project in projects:
        self.write([
          r'\begin{minipage}{\columnwidth}',
        ])

        self.print_project(project)

        self.write([
          r'\end{minipage}',
          r'\switchcolumn'
        ])

      self.write([
        r'\end{paracol}',
        r''
      ])
    
    self.write([
      # r'}',
      # r'\end{minipage}',
      r''
    ])

    self.write([
      # r'\begin{minipage}{0.67\textwidth}',
      # r'\fbox{'
      r'\restoregeometry'
    ])

    self.write([
      '\clearpage'
    ])

    self.write([
      r'\cvhead{Employment History}',
      r'',
      r'\cvsubsubhead{In order of employment}',
      r''
    ])

    

    for i in range(0, len(profile.employments), 3):
      empls = profile.employments[i:i+3]
      self.write([
        r'\columnratio{0.33}',
        r'\begin{paracol}{3}'
      ])

      for emp in empls:
        self.write([
          r'\begin{minipage}{\columnwidth}',
          # r'\fbox{'
        ])

        self.print_employment(emp)

        self.write([
          r'\end{minipage}',
          r'\switchcolumn'
        ])

      # self.write([
      #   r'\includegraphics[]{%s}' % employment
      # ])

      self.write([
        r'\end{paracol}'
      ])

    self.write([
      ''
    ])

    # self.write([
    #   r'\cvhead{Main Projects}',
    #   r'',
    #   r'\lipsum[1-30]'
    # ])

    # data += [empty_item]*20
    # for i in [0, 5, 7, 12]:
    #   data[i] = head_item

    # self.print_data_chain(data)

    self.write([
      # r'\end{paracol}',
      r'\end{document}'
    ])

    print('card_width=%f' % self.CARD_WIDTH)

