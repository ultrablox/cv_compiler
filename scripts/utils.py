from check import *
import os
import pathlib
import urllib.parse

def first_true(iterable, default=False, pred=None):
  """Returns the first true value in the iterable.

  If no true value is found, returns *default*

  If *pred* is not None, returns the first item
  for which pred(item) is true.

  """
  # first_true([a,b,c], x) --> a or b or c or x
  # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
  return next(filter(pred, iterable), default)

def latex_escape(msg):
  msg = msg.replace('_', '\_')
  msg = msg.replace('%', '\%')
  msg = msg.replace('#', '\#')
  return msg

def call_system(cmd_line):
  print('Calling: %s' % cmd_line)
  res = os.system(cmd_line)
  check_always(res == 0, 'Non-zero return code')

def ensure_dir_exists(file_path):
  dir_path = os.path.dirname(os.path.abspath(file_path))
  pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)

def svg_to_pdf(svg_path, pdf_path):
  ensure_dir_exists(pdf_path)
  call_system('inkscape --without-gui --export-pdf=%s %s 2> /dev/null' % (pdf_path, os.path.abspath(svg_path)))