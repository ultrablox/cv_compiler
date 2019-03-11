from tex_printer import *


class LetterDocument:
  def __init__(self, tex_printer):
    self._printer = tex_printer
    self._macros = self._printer.build_macros()

  def __enter__(self):
    self._printer.write([
      r'\documentclass[11pt,a4paper,sans]{moderncv}',
      r'\moderncvstyle{oldstyle}',
      r'\moderncvcolor{grey}',
      r'\usepackage[utf8]{inputenc} ',
      r'\usepackage[scale=0.75]{geometry}'
    ])

    self._printer.write(self._macros)

    self._printer.write([
      r'\begin{document}'
    ])

  def __exit__(self, type, value, tb):
    self._printer.write([
      r'\end{document}'
    ])


class LetterPrinter(TexPrinter):
  def __init__(self, out_fname, profile):
    # super().__init__(tmp_dir, rc_dirs)
    # self.__file_name = self.inner_file_path(file_name)
    self._pdfName = out_fname

    name_parts = profile.personal['name'].split(' ')
    self._firstName = name_parts[0]
    self._surname = name_parts[1]
    self._contacts = profile.contacts

    # self._role = 'ROLE NAME'
    # self._company = 'COMPANY NAME'

  def __enter__(self):
    self._tmpDir = tempfile.TemporaryDirectory()
    self.tmpDirName = self._tmpDir.name # #os.path.abspath('tmp')#
    self._texName = os.path.join(self.tmpDirName, 'main.tex')
    self._texFile = open(self._texName, 'w+')
    self.file = self._texFile
    self.rootDir = self.tmpDirName
    return self

  def __exit__(self, type, value, tb):
    self._texFile.close()
    call_system('cd {} && xelatex {} main.tex'.format(self.tmpDirName, ' '.join(self.TEX_ARGS)))
    shutil.copy(os.path.join(self.tmpDirName, 'main.pdf'), self._pdfName)

  def build_macros(self):
    return [
      r'\name{%s}{%s}' % (self._firstName, self._surname),
      r'\address{%s}{}{}' % self._contacts['residence'],
      r'\phone[mobile]{%s}' % self._contacts['phone'],
      r'\email{%s}' % self._contacts['email'],
      r'\homepage{%s}' % self._contacts['linkedin'],
      r'\newcommand{\vacancy}{%s}' % self._role,
      r'\newcommand{\company}{%s}' % self._company,
      r'\newcommand{\fullname}{%s %s}' % (self._firstName, self._surname)
    ]

  def print_heading(self):
    self.write([
      r'\recipient{%s HR}{}' % self._company,
      r'\date{\today}',
      r'\opening{Dear %s,}' % self._company,
      r'',
      r'',
      r'\closing{Sincerely,}',
      r'',
      r'\makelettertitle'
    ])

  def print(self, profile):
    company = 'Optiver'
    role = 'SOFTWARE DEVELOPER in AUTOMATED TRADING SYSTEMS'

    self.write([
      r'\documentclass[11pt,a4paper,sans]{moderncv}',   
      r'\moderncvstyle{oldstyle}',
      r'\moderncvcolor{grey}',
      r'\usepackage[utf8]{inputenc} ',
      r'\usepackage[scale=0.75]{geometry}',
      r'\name{%s}{%s}' % (self._firstName, self._surname),
      r'\address{%s}{}{}' % self._contacts['residence'],
      r'\phone[mobile]{%s}' % self._contacts['phone'],
      r'\email{%s}' % self._contacts['mail'],
      r'\homepage{%s}' % self._contacts['linkedin'],
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
