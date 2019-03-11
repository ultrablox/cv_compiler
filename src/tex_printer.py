
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


import os
from utils import *
from skill_matrix import *
from urllib.parse import urlparse
import sys
import tempfile
import glob
import shutil


class TexPrinterBase:
  TEX_ARGS = ['-halt-on-error', '--interaction=batchmode']

  def __init__(self):
    self.rcPaths = []
    self.rootDir = '.'

  def init_resources(self, rc_paths, root_dir):
    self.rcPaths = rc_paths
    self.rootDir = root_dir

  def writeln(self, data):
    self.file.write(data + '\n')

  def write(self, lines = []):
    for line in lines:
      self.writeln(line)

  def get_href(self, url, force_short=False):
    parsed_url = urlparse(url)
    label = '%s%s' % (parsed_url.netloc, parsed_url.path)
    if force_short:
      label = parsed_url.path

    return r'\httplink{%s}{%s}' % (latex_escape(parsed_url.geturl()), latex_escape(label))

  def find_resouce(self, base_path):
    assert self.rcPaths, 'No resource paths initialized!'
    for rc_dir in self.rcPaths:
      cur_path = os.path.join(rc_dir, base_path)
      if os.path.exists(cur_path) and os.path.isfile(cur_path):
        return os.path.abspath(cur_path)
    logging.debug('Resource not found: %s' % base_path)
    return None

  def image_path(self, base_path, size = None):
    path = self.find_resouce(base_path)
    if path:
      filename, extension = os.path.splitext(path)

      # If svg - convert to pdf into cached and return it
      if extension == '.svg':
        converted_fname = '%s.pdf' % filename[1:]
        converted_file_path = os.path.join(self.rootDir, '.converted', converted_fname) 
        svg_to_pdf(path, converted_file_path)
        return os.path.abspath(converted_file_path)
      elif extension == '.png':
        if size:
          size = [size[0] * 2, size[1] * 2]
          resized_fname = '%s_%dx%d%s' % (filename[1:], size[0], size[1], extension)
          converted_file_path = os.path.join(self.rootDir, '.converted', resized_fname)
          dest_dir = os.path.dirname(converted_file_path)
          print(dest_dir)
          pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
          call_system('convert %s -resize %dx%d %s' % (os.path.abspath(path), size[0], size[1], os.path.abspath(converted_file_path)))
          return os.path.abspath(converted_file_path)
        else:
          return os.path.abspath(path)
      else:
        return os.path.abspath(path)
    else:
      logging.error('Image not found: {}'.format(base_path))
      return ''

  def compile_to(self, entity, out_pdf):
    with tempfile.TemporaryDirectory() as tmp_dir:
      for file in glob.glob(r'../resources/styles/*.*') + glob.glob(r'../resources/fonts/*.*'):
        shutil.copy(file, tmp_dir)

      tex_file = os.path.join(tmp_dir, 'main.tex')
      with open(tex_file, 'w+') as f:
        self.file = f
        self.generate_body(entity)
        self.file = None
      compiled_pdf_name = call_latex(tmp_dir)
      shutil.copy(compiled_pdf_name, out_pdf)


class TexPrinter(TexPrinterBase):
  def __init__(self, root_dir, resources_paths = [], file = None):
    self.rootDir = root_dir
    self.rcPaths = resources_paths
    self.file = file

  def inner_file_path(self, path):
    return os.path.join(self.rootDir, path)

  def print_to(self, profile, path):
    with open(self.inner_file_path(path), 'w+') as file:
      self.file = file
      self.print_data(profile, file)
      self.file = None

  def print(self, profile, file_ref):
    self.file = file_ref
    self.print_data(profile)
    self.file = None

  def decorated_href(self, url):
    parsed_url = urlparse(url)
    decoration_img = 'img/internet.svg'
    if parsed_url.netloc == 'github.com':
      decoration_img = 'img/github_logo.svg'
    return '\\vcenteredinclude{%s} %s' % (self.image_path(decoration_img), self.get_href(url))

  def image(self, img, w):
    return r'\includegraphics[width=%dpt]{%s}' % (w, self.image_path(img))


class SingleCardPrinter(TexPrinterBase):
  def __init__(self, width, height):
    super().__init__()
    self.width = width
    self.height = height

  def generate_body(self, entity):
    self.write([
      r'\documentclass{ucv-cards}',
      r'\usepackage[margin=0pt,paperwidth=%dpt,paperheight=%dpt]{geometry}' % (self.width, self.height),
      r'\begin{document}',
    ])
    self.generate_content(entity)
    self.write([
      r'\end{document}'
    ])

