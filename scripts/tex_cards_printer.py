from tex_printer import *
from skill_matrix import *
from project_printer import *
from employment_printer import *

PT_IN_MM = 2.83465

# In pt
GRID_V_SPACING = 15
GRID_H_SPACING = 15
PAGE_H_MARGIN = 10*PT_IN_MM

# A4 =  210 mm x  297 mm =  595 pt x  842 pt
class TexCardsPrinter(TexPrinter):
  V_SPACING = 15
  CARD_WIDTH = (595 - 4 * V_SPACING)/3
  CARD_HEIGHT = 206
  CARDS_IN_ROW = 3
  HEADER_HEIGHT = 24
  HOR_SPACING = 4
  

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
      r'%s' % employment.role,
      r'',
      r'%s' % employment.name,
      r'',
      r'%s' % self.get_href(employment.web),
      r'',
      r'%s' % latex_escape(employment.description),
      r''
    ])
    
    self.write([
      r'{\rmfamily\fontsize{8}{8}\selectfont %s' % to_month_year(employment.period.startDate),
      r'%s\par}' % to_month_year(employment.period.endDate),
      ''
    ])
  
    notes = []

    if employment.projects:
      prj_names = []
      for prj in employment.projects:
        prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]
      note = 'worked in %s project%s' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')
      notes += [note]

    notes += employment.notes

    self.write([
      r'\begin{itemize-cv}'
    ])

    for note in notes:
      self.write([r'\item %s' % note])

    self.write([
      r'\end{itemize-cv}',
      r''
    ])

  
  def print_project(self, project):
    place = 'in %s' % project.parent.name if project.parent else 'hobby'
    period = project.get_period()

    self.write([
      r'%s' % (latex_escape(project.name)),
      r'',
      r'%d-%d' % (period.startDate.year, period.endDate.year),
      r'',
      r'%s' % self.get_href(project.webLink),
      # r'\raggedleft',
      # r'\cvirrelevant{%s}' % (to_month_year(period.startDate), to_month_year(period.endDate), place),
      r'',
      r'%s' % latex_escape(project.description),
      r'',
      r'%s' % latex_escape(', '.join(project.get_total_skill_list())),
      
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
   
    out_dir = self.rootDir
    self.write([
      r'\documentclass[10pt]{ucv-cards}',
      r'\usepackage[a4paper, top=10mm, bottom=20mm, left=%dpt, right=%dpt]{geometry}' % (PAGE_H_MARGIN, PAGE_H_MARGIN)
    ])

    # self.image_path('img/correct.svg')

    self.write([
      r'\begin{document}',
    #   r'\setlength\parindent{0pt}'
      ])


    self.write([
      r'\setlength{\parindent}{0pt}',
      r'\setlength{\columnsep}{50pt}',
      # r'\setlength{\intextsep}{0pt}',
      # r'\columnratio{0.33}',
      # r'\begin{paracol}{2}'
      # r'\begin{wrapfigure}{l}{180pt}',
      # r'\begin{minipage}[t][0.98\textheight]{180pt}'
    ])
    
    self.write([
      r'\begin{textblock}{%d}[0, 0](%f,%f)' % (self.CARD_WIDTH, PAGE_H_MARGIN, PT_IN_MM*10),
    ])

    self.print_head_column(profile)

    self.write([
      r'\end{textblock}'
    ])

    
    self.write([
      '\clearpage',
    ])

    self.write([
      # r'\begin{minipage}{0.67\textwidth}',
      # r'\fbox{'
      r'\newgeometry{top=10mm, bottom=20mm, left=%dpt, right=%dpt}' % (PAGE_H_MARGIN + self.CARD_WIDTH + GRID_H_SPACING, PAGE_H_MARGIN)
    ])
    
    front_page_projects_count = 6

    fp_projects = profile.projects[0:front_page_projects_count]
    other_projects = profile.projects[front_page_projects_count:]

    self.write([
        r'\cvhead{Main Projects}',
        r'',
        r'\cvsubsubhead{Relevant are first}',
      ])
    
    for i in range(0, len(fp_projects), 2):
      projects = fp_projects[i:i+2]
  
    # for project in profile.projects:
      self.write([
        r'\setlength{\columnsep}{%dpt}' % GRID_H_SPACING
      ])

      self.write([
        # r'\setcolumnwidth{%fpt,%fpt}' % (self.CARD_WIDTH, self.CARD_WIDTH),
        r'\columnratio{0.5}',
        r'\begin{paracol}{2}'
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
        r'\vspace{%dpt}' % GRID_V_SPACING,
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

    

    # self.write([
    #   r'\setlength{\columnsep}{%dpt}' % GRID_H_SPACING
    # ])
    self.write([
      r'\columnratio{0.33}',
    ])


    for i in range(0, len(other_projects), 3):
      projects = other_projects[i:i+3]
      self.write([
        r'\begin{paracol}{3}'
      ])

      for prj in projects:
        self.write([
          r'\begin{minipage}{\columnwidth}',
        ])

        self.print_project(prj)

        self.write([
          r'\end{minipage}',
          r'\switchcolumn'
        ])

      self.write([
        r'\end{paracol}'
        r'\vspace{%dpt}' % GRID_V_SPACING
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
        r'\begin{paracol}{3}'
      ])

      for emp in empls:
        self.write([
          r'\begin{minipage}{\columnwidth}',
        ])

        self.print_employment(emp)

        self.write([
          r'\end{minipage}',
          r'\switchcolumn'
        ])

      self.write([
        r'\end{paracol}'
        r'\vspace{%dpt}' % GRID_V_SPACING
      ])

    self.write([
      ''
    ])

    self.write([
      # r'\end{paracol}',
      r'\end{document}'
    ])

    print('card_width=%f' % self.CARD_WIDTH)

