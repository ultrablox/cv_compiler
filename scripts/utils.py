
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from check import *
import os
import pathlib
import urllib.parse
from transliterate import translit, get_available_language_codes
import re

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

def to_file_name(source_name):
  # trans_name = translit(source_name, 'en', reversed=True)
  trans_word = source_name
  # trans_word = re.sub(r'\W+', '', trans_word)
  trans_word = re.sub(r' ', '_', trans_word.lower())
  return trans_word

def is_scopus(pub):
  return ('source' in pub) and (pub['source'] == 'Scopus')