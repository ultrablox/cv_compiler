
from tex_printer import *

class LetterPrinter(TexPrinter):
  def __init__(self, tmp_dir, rc_dirs, file_name):
    super().__init__(tmp_dir, rc_dirs)
    self.__file_name = self.inner_file_path(file_name)

  def __enter__(self):
    self.file = open(self.__file_name, 'w+')
    return self

  def __exit__(self, type, value, tb):
    self.file.close()

  def print(self, profile):
    company = 'Flow Traders'
    role = 'C++ Software Engineer'

    name_parts = profile.personal['name'].split(' ')
    first_name = name_parts[0]
    surname = name_parts[1]

    self.write([
      r'\documentclass[11pt,a4paper,sans]{moderncv}',   
      r'\moderncvstyle{oldstyle}',
      r'\moderncvcolor{grey}',
      r'\usepackage[utf8]{inputenc} ',
      r'\usepackage[scale=0.75]{geometry}',
      r'\name{%s}{%s}' % (first_name, surname),
      r'\address{%s}{}{}' % profile.contacts['residence'],
      r'\phone[mobile]{%s}' % profile.contacts['phone'],
      r'\email{ultrablox@gmail.com} ',
      r'\homepage{%s}' % profile.contacts['linkedin'],
      r'\newcommand{\vacancy}{%s}' % role,
      r'\begin{document}',
      r'',
      r'\recipient{%s HR}{}' % company,
      r'\date{\today}',
      r'\opening{Dear %s,}' % company,
      r'',
      r'',
      r'\closing{Sincerely,}',
      r'',
      r'\makelettertitle',
      r'%s' % profile.lead,
      r'',
      r'I have enclosed my resume for your review and would be thankful for an opportunity to meet with you and discuss my application more detailed.',
      r'\makeletterclosing',
      r'',
      r'\end{document}'
    ])
