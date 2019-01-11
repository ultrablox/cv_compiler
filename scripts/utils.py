
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from check import *
import os
import pathlib
import urllib.parse
from transliterate import translit, get_available_language_codes
import re
import datetime
from datetime import date


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


def ensure_file_dir_exists(file_path):
  dir_path = os.path.dirname(os.path.abspath(file_path))
  pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)


def svg_to_pdf(svg_path, pdf_path):
  ensure_file_dir_exists(pdf_path)
  call_system('inkscape --without-gui --export-pdf=%s %s 2> /dev/null' % (pdf_path, os.path.abspath(svg_path)))


def to_file_name(source_name):
  # trans_name = translit(source_name, 'en', reversed=True)
  trans_word = source_name
  # trans_word = re.sub(r'\W+', '', trans_word)
  trans_word = re.sub(r' ', '_', trans_word.lower())
  return trans_word


def is_scopus(pub):
  return ('source' in pub) and (pub['source'] == 'Scopus')


def ensure_dir_exists(dir):
  pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


def serialize_array(items):
  res = []
  for item in items:
    res += [item.serialize()]
  return res


def serialize_array_to_property(dict, prop_name, items):
  dict[prop_name] = serialize_array(items)

def human_code_size(n):
  if n < 1000:
    return '%.1f' % (float(n) / 1000)
  elif n < 1000000:
    return '%.0fK' % (float(n) / 1000)
  else:
    return '%.1fM' % (float(n) / 1000000)

def to_month_year(time_point):
  return time_point.strftime('%b %Y')


def calculate_age(born):
  today = date.today()
  return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

