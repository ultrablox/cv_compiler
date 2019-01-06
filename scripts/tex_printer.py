
import os
from check import *
from utils import *
from basic_entities import *
from skill_matrix import *
from urllib.parse import urlparse
from log import *

class TexPrinter:
  def __init__(self, root_dir, resources_paths = []):
    self.rootDir = root_dir
    self.rcPaths = resources_paths
  
  def find_resouce(self, base_path):
    for rc_dir in self.rcPaths:
      cur_path = os.path.join(rc_dir, base_path)
      if os.path.exists(cur_path) and os.path.isfile(cur_path):
        # print(cur_path)
        return os.path.abspath(cur_path)
    log_print(LOG_LEVEL_DEBUG, 'Resource not found: %s' % base_path)
    return None

  def image_path(self, base_path):
    path = self.find_resouce(base_path)
    if path:
    # check_always(path, 'Referencing non-existing image: "%s"' % base_path)

      # Get extension
      filename, file_extension = os.path.splitext(path)

      # If svg - convert to pdf into cached and return it
      if file_extension == '.svg':
        converted_fname = '%s.pdf' % filename[1:]

        converted_file_path = os.path.join(self.rootDir, '.converted', converted_fname)#, 
        # print(converted_file_path)
        svg_to_pdf(path, converted_file_path)
        # print(converted_file_path)
        # exit(1)

        return converted_file_path
      else:
        return path
    else:
      log_print(LOG_LEVEL_DEBUG, 'Image not found: %s' % base_path)
      return ''

  def inner_file_path(self, path):
    return os.path.join(self.rootDir, path)

  def print_to(self, profile, path):
    with open(self.inner_file_path(path), 'w+') as file:
      self.file = file
      self.print_data(profile, file)
      self.file = None

  def print(self, profile, file_ref):
    self.file = file_ref
    self.print_data(profile)
    self.file = None

  def writeln(self, data):
    self.file.write(data + '\n')

  def write(self, lines = []):
    for line in lines:
      self.writeln(line)

  def get_href(self, url, force_short = False):
    parsed_url = urlparse(url)
    label = '%s%s' % (parsed_url.netloc, parsed_url.path)
    if force_short:
      label = parsed_url.path
    return '\href{%s}{%s}' % (parsed_url.geturl(), label)

class ContactsPrinter(TexPrinter):
  def print_data(self, profile):
    self.write(['\\blocksection{Personal and Contact Info}{'])

    head_line = 'Name: %s \splitter Sex: %s \splitter Date of birth: %s \splitter Nationality: %s' % (profile.personal['name'], profile.personal['sex'], profile.personal['birthdate'], profile.personal['nationality'])

    if profile.personal['additional']:
      head_line += '\splitter %s' % profile.personal['additional']
    head_line += '\hfill \\break'

    self.writeln(head_line)
    self.writeln('%s \hfill \\break' % profile.contacts['residence'])

    contacts_str = '\\vcenteredinclude{%s} \href{mailto:%s}{%s}\n' % (self.image_path('img/email.svg'), profile.contacts['email'], profile.contacts['email'])

    # Phone
    contacts_str += '\\vcenteredinclude{%s} %s\n' % (self.image_path('img/phone.svg'), profile.contacts['phone'])

    # Linked in
    contacts_str += '\\vcenteredinclude{%s} %s\n' % (self.image_path('img/linkedin.svg'), self.get_href(profile.contacts['linkedin'], True))

    # Skype
    contacts_str += '\\vcenteredinclude{%s} %s \\\\' % (self.image_path('img/skype.svg'), profile.contacts['skype'])
    self.writeln(contacts_str)

    self.writeln('\\textbf{Languages:} %s\n' % ', '.join(profile.contacts['languages']))
    self.write(['\\vspace{\\blocksep}',
      '}'])

def human_code_size(n):
  if n < 1000:
    return '%d' % n
  elif n < 1000000:
    return '%.0fK' % (float(n) / 1000)
  else:
    return '%.1fM' % (float(n) / 1000000)

class ProjectsPrinter(TexPrinter):
  def skills_line(self, prj):
    all_skills = prj.get_total_skill_list()
    if all_skills:
      return '\skills{%s}' % latex_escape(', '.join(all_skills))
    else:
      return ''

  def print_project_data(self, prj):
    self.writeln("\project{%s}{%s}" % (latex_escape(prj.name), self.image_path(os.path.join('img', prj.icon))))
    self.writeln("{%d-%s}" % (prj.period.startDate.year, 'present' if prj.period.isOpen else str(prj.period.endDate.year)))
    if prj.parent:
        self.writeln('{in %s}' % prj.parent.name)
    else:
        self.writeln('{HOBBY}')

    self.writeln("{%s}{" % (prj.description))
    first_line_items = []

    first_line_items += ["\\teamsize{%s}" % (prj.teamSize)]

    first_line_items += ["\\codesize{%s}" % human_code_size(prj.linesOfCode)]

    if prj.webLink:
        url = urllib.parse.urlparse(prj.webLink)
        label = url.netloc
        if url.path:
            label += url.path
        first_line_items += ['\weblink{%s}{%s}' % (latex_escape(prj.webLink), latex_escape(label))]

    # first_line_items += [type_str] 
    self.writeln("\item %s" % ' '.join(first_line_items))
    skills = self.skills_line(prj)
    if skills:
      self.writeln('\item %s' % skills)
    self.writeln("}{charon:project}" )

    # Tasks
    for task in prj.tasks:
      self.writeln("%s" % latex_escape(task.description))
      self.writeln('\\begin{itemize-noindent}')
      for ach in task.achievements:
        self.writeln("\item[] \\achievement{%s}" % latex_escape(ach))
      self.writeln('\\end{itemize-noindent}')

    # for achievement in prj.achievements:
    #     self.writeln("\item \\achievement{%s}\n" % (latex_escape(achievement)))
    # if len(prj.notes) != 0:
    #     self.writeln("\item %s\n" % latex_escape('; '.join(prj.notes)))
    

  def print_data(self, profile):
    self.write(['\\blocksection{Main Projects}{'])
    sorted_projects = sorted(profile.projects, key=lambda prj: prj.period.startDate, reverse=True)
    for prj in sorted_projects:
      self.print_project_data(prj)
      self.writeln('\\vspace{\\blocksep}')
    self.write(['}'])

class EmploymentsPrinter(TexPrinter):
  def print_data(self, profile):
    self.writeln('\\blocksection{Employment History}{')
    for employment in profile.employments:
      self.writeln("\job{%s}{%s}{%s}{%s}{%s}{%s}{\n" % (employment.period.startDate.strftime('%b %Y'), 'Present' if employment.period.isOpen else employment.period.endDate.strftime('%b %Y'), employment.name, employment.web, employment.role, employment.description))
      self.writeln("\t\\begin{itemize-noindent}")
      
      prj_names = []
      for prj in employment.projects:
          prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]

      notes_arr = ['\t\t\item{ worked in %s project%s}' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')]

      for note in employment.notes:
          notes_arr += ['\t\t\item{%s}' % note]

      self.write(notes_arr)
      # self.writeln("")
      self.writeln("\t\end{itemize-noindent}")
      self.writeln("}{%s}" % self.image_path(employment.logo))
    self.write(['}'])

class EducationsPrinter(TexPrinter):
  def print_facility_data(self, degree, facility, period, gpa, web = None, notes = []):
    head_line = '%d-%d --- \\textbf{%s}, %s' % (period.startDate.year, period.endDate.year, degree, facility)
    if web:
      head_line += ' (%s)' % self.get_href(web)
    head_line += ', %s' % latex_escape(gpa)
    self.write([head_line])

    self.write(['\\begin{itemize-noindent}'])
    for note in notes:
      self.write(['\item %s' % note])
    self.write(['\end{itemize-noindent}'])

  def print_facility(self, facility):
    self.print_facility_data(facility['degree'],
        facility['facility'], 
        TimePeriod(facility['period']),
        facility['gpa'],
        facility['web'],
        facility['notes']
      )
    self.write(['\\vspace{\\blocksep}'])

  def print_data(self, profile):
    self.write(['\\blocksection{Education}{'])
    for edu in profile.education:
      self.print_facility(edu)
    self.write(['}'])


class ActivitiesPrinter(TexPrinter):
  def print_data(self, profile):
    if not profile.has_activities():
      return
    self.writeln('\\blocksection{Professional Activities}{')

    # Scientific are most valuable
    if profile.scientificPubs:
      summary_str = '%d total' % len(profile.scientificPubs)
      if profile.scopus_publication_count():
        summary_str += ', incl. %d Scopus' % profile.scopus_publication_count()
      self.write(['\t\\textbf{Recent Scientific Publications} (%s)' % summary_str,
        '\t\\begin{itemize-noindent}'])
      for pub in profile.scientificPubs:
        if pub['visible']:
          is_scopus = '\scopus' if (('source' in pub) and (pub['source'] == 'Scopus')) else ''
          self.writeln('\item %d --- %s // %s %s' % (int(pub['year']), pub['title'], pub['journal'], is_scopus))

      self.writeln('\t\end{itemize-noindent}')

    # Popular publications are less important
    if profile.popularPubs:
      years = int(profile.popularPubs[0]['year']) - int(profile.popularPubs[-1]['year']) + 1
      summary_str = '%d total, avg. %.1f publicatons / year' % (len(profile.popularPubs), float(len(profile.popularPubs))/years)
      self.write(['\t\\textbf{Recent Popular Publications} (%s):' % summary_str,
        '\\begin{itemize-noindent}'
      ])
      for pub in profile.popularPubs:
        if pub['visible']:
          self.writeln('\item \ppublication{%d}{%s}{%s}{%s}' % (int(pub['year']), pub['title'], pub['source'], pub['url']))
      self.writeln('\end{itemize-noindent}')

    # Conferences are the least important
    if profile.conferences:
      years = int(profile.conferences[0]['year']) - int(profile.conferences[-1]['year']) + 1
      summary_str = '%d total, avg. %.1f presentations / year' % (len(profile.conferences), float(len(profile.popularPubs))/years)
      conf_strs = []
      for conf in profile.conferences:
        conf_strs += ['%s (%s, %d)' % (conf['name'], conf['location'], conf['year'])]
      self.writeln("\t\\textbf{Speaker of} (%s): %s, etc." % (summary_str, ' '.join(conf_strs)))

    self.write(['\\vspace{\\blocksep}',
      '}'])

class LeadPrinter(TexPrinter):
  def print_data(self, profile):
    self.write(['\\blocksection{Objective and Summary}{',
      '\t%s' % profile.lead,
      '\t\\vspace{\\blocksep}',
      '}'
    ])

class TraitsPrinter(TexPrinter):
  def print_data(self, profile):
    self.write(['\\blocksection{Interests and Personal Traits}{',
      '\t\\begin{itemize-noindent}'])

    for trait in profile.traits:
      self.write(['\item \\textbf{%s:} %s' % (trait['name'], trait['details'])])

    self.write(['\\end{itemize-noindent}',
      '}'
    ])

class SkillsPrinter(TexPrinter):
  def print_data(self, profile):
    self.write(['\\blocksection{Professional Skills}{'])

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
        
        self.writeln('\\textbf{%s:} %s \\newline' % (group_name, ', '.join(skills)))

    for sgr in profile.specialSkillGroups:
      self.write(['\skillgroup{%s:}{%s}{' % (sgr['name'], sgr['details'])])
      for adv in sgr['advantages']:
          self.write(['\item %s' % adv])
      self.write(['}'])

    self.write(['\\vspace{\\blocksep}',
      '}'])


class TexCVPrinter(TexPrinter):
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
        '\\vcenteredinclude{%s} #1' % self.image_path('img/star.svg'),
      '}',
      '\\newcommand{\skills}[1]{',
        '\\vcenteredinclude{%s} #1' % self.image_path('img/idea.svg'),
      '}'])

  def print_data(self, profile, file):
    page_profile = self.PAGE_PROFILES[self.paperSize]
    margins = page_profile['margins']
    self.write([
      '\documentclass[10pt]{article}',
      '\\usepackage[%spaper, top=%dmm, bottom=%dmm, left=%dmm, right=%dmm]{geometry}' % (self.paperSize, margins[0], margins[1], margins[2], margins[3]),
      # '\\usepackage[a5paper, top=10mm, bottom=7mm, includehead, includefoot]{geometry}',
      '\\usepackage{fancyhdr}',
      '' if self.paperSize == 'a5' else '\\pagestyle{fancy}',
      '\\fancyhf{}',
      '\\fancyhead[R]{%s}' % profile.personal['name'],
      '\\fancyhead[C]{\\thepage}',
      '\\lhead{\setlength{\\unitlength}{1pt}',
      '\\begin{picture}(0,0)',
      '\put(-36,-10){\includegraphics[width=28pt]{%s}}' % self.image_path('watermark.svg'),
      '\end{picture}}',
      '\input{styles.tex}',
      '\\renewcommand{\headrulewidth}{0.4pt}'
    ])
    self.print_styles()
    self.write([
      '\\begin{document}'
      ])

    printers = [ContactsPrinter, LeadPrinter, EducationsPrinter, SkillsPrinter, ProjectsPrinter, EmploymentsPrinter, ActivitiesPrinter, TraitsPrinter]
    for printer in printers:
      printer(self.rootDir, self.rcPaths).print(profile, self.file)

    self.write(['\end{document}'])
      
