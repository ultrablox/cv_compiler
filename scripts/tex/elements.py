
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
