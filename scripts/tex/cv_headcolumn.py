from utils import *
from cv.time import *
from cv.skill_experience import *
from tex.elements import *

class HeadColumn:
  def __init__(self, tex_printer, profile):
    self.__printer = tex_printer
    self.__profile= profile
    self.print()

  def print(self):
    # Personal
    self.print_personal()
    self.print_contacts()

    # Objective
    self.__printer.write([
      r'\cvhead{About me}'
    ])

    self.__printer.write([  
      r'\cvnormal %s' % self.__profile.lead,
      r'',
      r'\colsectionspace'
    ])

    # Education
    self.__printer.write([
      r'\cvhead{Education}',
      r''
    ])
    self.print_education(self.__profile.education)
    self.__printer.write([  
      r'\colsectionspace',
      r''
    ])

    # Skills
    self.__printer.write([
      r'\cvhead{Skills}',
      r'',
      r'\colsubhead{Disired highlighted}',
      r''
    ])
    self.print_skills(self.__profile.skills_totals())

  def print_skills(self, skills):
    VISUAL_SKILL_COUNT = 20
    self.print_skill_chart(skills[:VISUAL_SKILL_COUNT])
    self.print_skill_list(skills[VISUAL_SKILL_COUNT:])

  
  def print_personal(self):
    age = calculate_age(datetime.datetime.strptime(self.__profile.personal['birthdate'], '%d.%m.%Y'))
    
    with MinipageElement(self.__printer, r'0.3\columnwidth'):
      self.__printer.write([
        r'\fbox{\includegraphics[width=0.9\textwidth,keepaspectratio]{%s}}' % self.__printer.image_path('img/photo.jpg', [62,62]),
        # r'\photo{%s}{0.3\columnwidth}' % self.image_path('img/photo.jpg', [62,62]),
      ])

    self.__printer.write([
      r'\hspace{2pt}'
    ])

    with MinipageElement(self.__printer, r'0.67\columnwidth'):
      self.__printer.write([
        r'\cvhead{%s}' % self.__profile.personal['name'],
        r'',
        r'%s, %s y.o.' % (self.__profile.personal['sex'], age),
        r'',
        r'Residence: %s' % self.__profile.contacts['residence'],
        r'',
        r'Citizenship: %s' % self.__profile.personal['nationality'],
        r'',
      ])

    self.__printer.write([
      r'',
      r'\colsectionspace'
    ])
    

  def print_contacts(self):
    self.__printer.write([
      r'\noindent\textcolor{color1}{\rule{\columnwidth}{0.5pt}}',
      r''
    ])

    linkedin_name = self.__profile.contacts['linkedin'].split('/')[-1]
    
    with MinipageElement(self.__printer, r'0.38\columnwidth'):
      self.__printer.write([
        r'\vcenteredinclude{%s}' % self.__printer.image_path('img/linkedin.svg'),
        r'\rmfamily %s' % linkedin_name,
        r'',
        r'\vcenteredinclude{%s}' % self.__printer.image_path('img/skype.svg'),
        r'\rmfamily %s' % (self.__profile.contacts['skype'])
      ])
    
    with MinipageElement(self.__printer, r'0.58\columnwidth'):
      self.__printer.write([
        r'\raggedleft',
        r'\rmfamily \href{mailto:%s}{%s}' % (self.__profile.contacts['email'], self.__profile.contacts['email']),
        r'\vcenteredinclude{%s}' % self.__printer.image_path('img/email.svg'),
        r'',
        r'\rmfamily %s' % (self.__profile.contacts['phone']),
        r'\vcenteredinclude{%s}' % self.__printer.image_path('img/phone.svg'),
      ])
    self.__printer.write([
      r'',
      r'\noindent\textcolor{color1}{\rule{\columnwidth}{0.5pt}}',
      r'',
      r'\colsectionspace',
      r''
    ])

  def print_facility_data(self, degree, facility, period, gpa, web = None, notes = []):
    self.__printer.write([
      r'{\rmfamily\fontsize{12}{12}\selectfont %d - \textbf{%s}\par}' % (period.endDate.year, degree),
      '',
      r'%s' % (facility),
      r'',
      r'%s | %s' % (latex_escape(gpa), self.__printer.get_href(web)),
      r''
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
      VSpacingElement(self.__printer, 6)

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

        self.__printer.writeln(r'\cvnormal \textbf{%s:} %s \newline' % (group_name, ', '.join(skills)))


  def print_skill_chart(self, skills):
    skills.reverse()
    if not skills:
      return
    max_value = skills[0]['size']
    visual_count = len(skills)

    coords = ['{%s}' % latex_escape(x['name']) for x in skills]

    self.__printer.write(['\pgfplotsset{',
      'compat=1.13,',
      r'tick label style = {font=\cvnormal},',
      r'every axis label = {font=\cvnormal},',
      r'legend style = {font=\cvnormal},',
      r'label style = {font=\cvnormal},',
      r'}'
    ])

    self.__printer.write([r'\begin{tikzpicture}',
      r'\begin{axis}[',
      r'font=\cvnormal,',
      r'xlabel={Experience, years},',
      r'xbar stacked,',
      r'width=0.9\columnwidth,',
      r'xtick=\empty,',
      r'ytick=data,',
      r'axis y line*=none,',
      r'axis x line*=top,',
      # r'axis y line style={draw=none},',
      r'bar width=10pt,',
      r'yticklabels={%s},' % ','.join(coords),
      r'xmin=0,',
      r'area legend,',
      r'clip=false,',
      r'enlarge y limits=0.03,',
      r'y=0.45cm,',
      r'height=200pt,',
      r'nodes near coords,',
      r'every node near coord/.append style={at ={(\pgfplotspointmeta,\pgfplotspointy)},anchor=west, xshift=-5pt},',
      r'every node near coord/.append style={/pgf/number format/.cd, fixed, fixed zerofill, precision=1},',
      r'every node near coord/.append style={/pgf/number format/assume math mode},',
      r'visualization depends on=y \as \pgfplotspointy,',
      r'every axis plot/.append style={fill},',
      r']'
    ])

    labels = ['Desired', 'Job\'s a job', 'Prefferably avoid']
    colors = ['color1', 'color3', 'color3']

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

      self.__printer.write([
        r'\addplot[fill=%s%s, draw=none] coordinates {%s};' % (colors[i], format_str, latex_escape(' '.join(x_coords))),
      ])

    self.__printer.write([
      r'\end{axis}',
      r'\end{tikzpicture}',
      r'\newline'
    ])
