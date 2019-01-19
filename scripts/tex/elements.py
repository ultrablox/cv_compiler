
class MinipageElement:
  def __init__(self, tex_printer, w = r'\textwidth'):
    self.__printer = tex_printer
    self.__width = w

  def __enter__(self):
    self.__printer.write([
      r'\begin{minipage}{%s}' % self.__width
    ])

  def __exit__(self, type, value, tb):
    self.__printer.write([
      r'\end{minipage}'
    ])

class VSpacingElement:
  def __init__(self, tex_printer, spacing):
    self.__printer = tex_printer
    self.__spacing = spacing
    self.print()

  def print(self):
    self.__printer.write([
      r'',
      r'\vspace{%dpt}' % self.__spacing,
      r''
    ])


class SectionElement:
  def __init__(self, tex_printer):
    self.__printer = tex_printer

  def __enter__(self):
    self.__printer.write([
      r'\begin{multicols}{3}'
    ])

  def __exit__(self, type, value, tb):
    self.__printer.write([
      r'\end{multicols}'
    ])


class SectionHeading:
  def __init__(self, tex_printer, head, subhead, indent = 0):
    self.__printer = tex_printer
    self.__head = head
    self.__subhead = subhead
    self.__spacing = indent
    self.print()

  def print(self):
    space = ''
    col_width = '\columnwidth'
    if self.__spacing:
      space = r'\hspace{%dpt}' % self.__spacing
      col_width = '{\columnwidth-%dpt}' % self.__spacing

    self.__printer.write([
      r'%s\textcolor{color1}{\noindent\rule{%s}{0.5pt}}' % (space, col_width),
      r'',
      r'%s\cvhead{%s}' % (space, self.__head),
      r'',
      r'%s\cvsubsubhead{%s}' % (space, self.__subhead),
      r'',
      r'%s\textcolor{color1}{\noindent\rule{%s}{0.5pt}}' % (space, col_width),
    ])

