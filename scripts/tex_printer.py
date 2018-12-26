
import os
from check import *
from utils import *

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
