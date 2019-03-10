
class MinipageElement:
  def __init__(self, tex_printer, w = r'\textwidth', opt_params = ''):
    self.__printer = tex_printer
    self.__width = w
    self.__params = opt_params

  def __enter__(self):
    self.__printer.write([
      r'\begin{minipage}%s{%s}' % (self.__params, self.__width)
    ])

  def __exit__(self, type, value, tb):
    self.__printer.write([
      r'\end{minipage}'
    ])

class VSpacingElement:
  def __init__(self, tex_printer, spacing):
    assert isinstance(spacing, int) or isinstance(spacing, float), 'Provide number to VSpacingElement'

    self.__printer = tex_printer
    self.__spacing = spacing
    self.print()

  def print(self):
    self.__printer.write([
      r'\vspace{%dpt}' % self.__spacing
    ])


class VSpaceGuard:
  def __init__(self, tex_printer, spacing):
    self.__printer = tex_printer
    self.__spacing = spacing

  def __enter__(self):
    VSpacingElement(self.__printer, self.__spacing / 2)

  def __exit__(self, type, value, tb):
    VSpacingElement(self.__printer, self.__spacing / 2)


class SectionElement:
  def __init__(self, tex_printer):
    self.__printer = tex_printer

  def __enter__(self):
    self.__printer.write([
      r'\begin{multicols}{3}',
      r'\cvsectionbegin'
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
    space = r'\headoffset{%d}' % self.__spacing
    # col_width = '\columnwidth'
    col_width = '\headlinelen{%d}' % self.__spacing
    # if self.__spacing:
    #   col_width = '{\columnwidth-%dpt}' % self.__spacing

    self.__printer.write([
      r'%s\textcolor{color1}{\noindent\rule{%s}{0.5pt}}' % (space, col_width),
      r'',
      r'%s\cvhead{%s}' % (space, self.__head),
      r'',
      r'%s\cvsubsubhead{%s}' % (space, self.__subhead),
      r'',
      r'%s\textcolor{color1}{\noindent\rule{%s}{0.5pt}}' % (space, col_width),
    ])


class Document:
  def __init__(self, tex_printer, h_margin):
    self._printer = tex_printer
    self._hMargin = h_margin

  def __enter__(self):
    self._printer.write([
      r'\documentclass[10pt]{ucv-cards}',
      r'\usepackage[a4paper, top=10mm, bottom=20mm, left=%dmm, right=%dmm]{geometry}' % (self._hMargin, self._hMargin),
      r'\begin{document}'
    ])

  def __exit__(self, type, value, tb):
    self._printer.write([
      r'\end{document}'
    ])


class TextBlock:
  def __init__(self, printer, width, anchor_x, anchor_y, x, y):
    self._printer = printer
    self._width = width
    self._anchorX = anchor_x
    self._anchorY = anchor_y
    self._x = x
    self._y = y

  def __enter__(self):
    self._printer.write([
      r'\begin{textblock}{%d}[%f, %f](%d,%d)' % (self._width, self._anchorX, self._anchorY, self._x, self._y)
    ])

  def __exit__(self, type, value, tb):
    self._printer.write([
      r'\end{textblock}'
    ])


class Itemize:
  def __init__(self, tex_printer):
    self._printer = tex_printer

  def __enter__(self):
    self._printer.write([
      r'\begin{itemize-cv}'
    ])
    return self

  def item(self, text):
    self._printer.write([
      r'\item {}'.format(text)
    ])

  def __exit__(self, type, value, tb):
    self._printer.write([
      r'\end{itemize-cv}'
    ])

