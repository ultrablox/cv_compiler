
import os
from check import *
from utils import *
from basic_entities import *
from skill_matrix import *

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
      return ''

  def inner_file_path(self, path):
    return os.path.join(self.rootDir, path)

  def print(self, profile, path):
    with open(self.inner_file_path(path), 'w+') as file:
      self.print_data(profile, file)

class StylesPrinter(TexPrinter):
  def print_data(self, profile, file):
    file.writelines([
      '\\newcommand{\weblink}[2]{',
         '\\vcenteredinclude{%s} \href{#1}{#2}' % self.image_path('img/internet.svg'),
        '}\n\n'])

    file.writelines([
      '\\newcommand{\\teamsize}[1]{',
        '\\vcenteredinclude{%s}  #1' % self.image_path('img/man.svg'),
      '}\n\n'])

    file.writelines([
      '\\newcommand{\\achievement}[1]{',
        '\\vcenteredinclude{%s} #1' % self.image_path('img/star.svg'),
      '}\n\n'])
  
    file.writelines([
      '\\newcommand{\skills}[1]{',
        '\\vcenteredinclude{%s} #1' % self.image_path('img/idea.svg'),
      '}\n\n'])

class ContactsPrinter(TexPrinter):
  def print_data(self, profile, file):
    file.write('Name: %s \splitter Sex: %s \splitter Date of birth: %s \splitter Nationality: %s \splitter %s \hfill \\break\n' % (profile.personal['name'], profile.personal['sex'], profile.personal['birthdate'], profile.personal['nationality'], profile.personal['additional']))
    file.write('%s \hfill \\break\n' % profile.contacts['residence'])
    file.write('\\vcenteredinclude{%s} \href{mailto:%s}{%s}\n' % (self.image_path('img/email.svg'), profile.contacts['email'], profile.contacts['email']))
    file.write('\\vcenteredinclude{%s} %s\n' % (self.image_path('img/phone.svg'), profile.contacts['phone']))
    file.write('\\vcenteredinclude{%s} \href{%s}{%s}\n' % (self.image_path('img/linkedin.svg'), profile.contacts['linkedin'], profile.contacts['linkedin']))
    file.write('\\vcenteredinclude{%s} %s \\\\\n' % (self.image_path('img/skype.svg'), profile.contacts['skype']))
    file.write('\\textbf{Languages:} %s\n' % ', '.join(profile.contacts['languages']))

class ProjectsPrinter(TexPrinter):
  def print_data(self, profile, file):
    sorted_projects = sorted(profile.projects, key=lambda prj: prj.period.startDate, reverse=True)
    for prj in sorted_projects:
      file.write("\project{%s}{%s}" % (latex_escape(prj.name), self.image_path(os.path.join('img', prj.icon))))
      file.write("{%d-%s}" % (prj.period.startDate.year, 'present' if prj.period.isOpen else str(prj.period.endDate.year)))
      if prj.parent:
          file.write('{in %s}' % prj.parent.name)
      else:
          file.write('{HOBBY}')

      file.write("{%s}{" % (prj.description))
      first_line_items = []
      # type_str = "$\\bullet$"
      # if prj.parent:
      #     type_str += " in %s" % prj.parent.name
      # else:
      #     type_str += " hobby"

      first_line_items += ["\\teamsize{%s}" % (prj.teamSize)]

      if prj.webLink:
          url = urllib.parse.urlparse(prj.webLink)
          label = url.netloc
          if url.path:
              label += url.path
          first_line_items += ['\weblink{%s}{%s}' % (latex_escape(prj.webLink), latex_escape(label))]

      # first_line_items += [type_str] 
      file.write("\item %s\n" % ' '.join(first_line_items))
      if len(prj.skills) != 0:
          file.write("\item \skills{%s}\n" % latex_escape(', '.join(prj.skills)))
      for achievement in prj.achievements:
          file.write("\item \\achievement{%s}\n" % (latex_escape(achievement)))
      if len(prj.notes) != 0:
          file.write("\item %s\n" % latex_escape('; '.join(prj.notes)))
      file.write("}{charon:project}\n" )

class EmploymentsPrinter(TexPrinter):
  def print_data(self, profile, file):
    for employment in profile.employments:
      file.write("\job{%s}{%s}{%s}{%s}{%s}{%s}{\n" % (employment.period.startDate.strftime('%b %Y'), 'Present' if employment.period.isOpen else employment.period.endDate.strftime('%b %Y'), employment.name, employment.web, employment.role, employment.description))
      file.write("\t\\begin{itemize-noindent}\n")
      
      prj_names = []
      for prj in employment.projects:
          prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]

      notes_arr = ['\t\t\item{ worked in %s project%s}' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')]

      for note in employment.notes:
          notes_arr += ['\t\t\item{%s}' % note]

      file.write("\n".join(notes_arr))
      file.write("\n")
      file.write("\t\end{itemize-noindent}\n")
      file.write("}{%s}\n" % self.image_path(employment.logo))

class EducationsPrinter(TexPrinter):
  def print_data(self, profile, file):
    for edu in profile.education:
      tp = TimePeriod(edu['period'])
      file.write('\education{%s}{%d-%d}{%s}{%s}{' % (edu['place'], tp.startDate.year, tp.endDate.year, edu['name'], latex_escape(edu['gpa'])))
      if ('notes' in edu) and (len(edu['notes']) > 0):
          file.write('\\begin{itemize-noindent}')
          notes_arr = []
          for note in edu['notes']:
              notes_arr += ['\item %s' % note]
          file.write('\n'.join(notes_arr))
          file.write('\end{itemize-noindent}')
      file.write('}')


class ActivitiesPrinter(TexPrinter):
  def print_data(self, profile, file):
    if not profile.has_activities():
      return
    file.write('\\blocksection{Professional Activities}{\n')

    # Scientific are most valuable
    if profile.scientificPubs:
      summary_str = '%d total' % len(profile.scientificPubs)
      if profile.scopus_publication_count():
        summary_str += ', incl. %d Scopus' % profile.scopus_publication_count()
      file.writelines(['\t\\textbf{Recent Scientific Publications} (%s)\n' % summary_str,
        '\t\\begin{itemize-noindent}\n'])
      for pub in profile.scientificPubs:
        if pub['visible']:
          is_scopus = '\scopus' if (('source' in pub) and (pub['source'] == 'Scopus')) else ''
          file.write('\item %d --- %s // %s %s\n' % (int(pub['year']), pub['title'], pub['journal'], is_scopus))

      file.write('\t\end{itemize-noindent}\n')

    # Popular publications are less important
    if profile.popularPubs:
      years = int(profile.popularPubs[0]['year']) - int(profile.popularPubs[-1]['year']) + 1
      summary_str = '%d total, avg. %.1f publicatons / year' % (len(profile.popularPubs), float(len(profile.popularPubs))/years)
      file.writelines(['\t\\textbf{Recent Popular Publications} (%s):\n' % summary_str])
      file.write('\\begin{itemize-noindent}\n')
      for pub in profile.popularPubs:
          file.write('\item \ppublication{%d}{%s}{%s}{%s}' % (int(pub['year']), pub['title'], pub['source'], pub['url']))
      file.write('\end{itemize-noindent}\n')

    # Conferences are the least important
    if profile.conferences:
      years = int(profile.conferences[0]['year']) - int(profile.conferences[-1]['year']) + 1
      summary_str = '%d total, avg. %.1f presentations / year' % (len(profile.conferences), float(len(profile.popularPubs))/years)
      file.write('\t\\textbf{Speaker of} (%s): ' % summary_str)
      conf_strs = []
      for conf in profile.conferences:
        conf_strs += ['%s (%s, %d)' % (conf['name'], conf['location'], conf['year'])]
      file.write("%s, etc.\n" % ' '.join(conf_strs))

    file.writelines(['\\vspace{\\blocksep}',
      '}'])



class TraitsPrinter(TexPrinter):
  def print_data(self, profile, file):
    for trait in profile.traits:
      file.write('\item \\textbf{%s:} %s\n' % (trait['name'], trait['details']))

class SkillsPrinter(TexPrinter):
  def print_data(self, profile, file):
    file.write('\\blocksection{Professional Skills}{\n')

    skill_matrix = SkillMatrix(profile)
    skill_matrix.generate(file)

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
        
        
        file.write('\\textbf{%s:} %s\n\n' % (group_name, ', '.join(skills)))

    for sgr in profile.specialSkillGroups:
      file.write('\skillgroup{%s:}{%s}{\n' % (sgr['name'], sgr['details']))
      for adv in sgr['advantages']:
          file.write('\item %s\n' % adv)
      file.write('}\n')

    file.write('\t\\vspace{\\blocksep}\n')
    file.write('}\n\n')
