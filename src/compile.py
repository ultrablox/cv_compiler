#!/usr/bin/env python3

# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


# from skill_attitude import *
import json
import datetime

import urllib.parse
import sys
import os
import argparse
from skill_matrix import *
import glob
import shutil
from tex_cards_printer import *
from cv.employee_profile import *
from db import skills_db
import qrcode
import qrcode.image.svg
import tempfile
from tex.cl_printer import *


def print_qr_code(file_name):
  qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=128,
        border=0,
    )
  qr.add_data('https://github.com/ultrablox/cv_compiler')
  qr.make(fit=True)

  img = qr.make_image(fill_color="black", back_color="white", image_factory=qrcode.image.svg.SvgImage)
  img.save(file_name)


def add_bool_arg(parser, name, default=False):
  group = parser.add_mutually_exclusive_group(required=False)
  group.add_argument('--' + name, dest=name, action='store_true')
  group.add_argument('--no-' + name, dest=name, action='store_false')
  parser.set_defaults(**{name:default})


def main():
  logging.basicConfig(level=logging.INFO)
  
  parser = argparse.ArgumentParser(description='Compile CV into PDF file.')
  parser.add_argument('--input_dir', type=str, default='/input', help='input profile directory')
  # parser.add_argument('--paper_size', type=str, default='a4', choices=['a4', 'a5'], help='Paper size')
  add_bool_arg(parser, 'watermark', True)
  args = parser.parse_args()

  # Check necessary paths exist
  assert os.path.exists(args.input_dir), 'Input directory "%s" does not exist' % args.input_dir
  out_dir = os.path.abspath(os.path.join('..', 'out'))
  assert os.path.exists(out_dir), 'Output directory "%s" does not exist' % out_dir

  # Load input data
  skill_db = skills_db.SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  profile = EmployeeProfile(skill_db)
  profile.load(args.input_dir)

  profile.compress()

  with tempfile.TemporaryDirectory() as tmp_dir:
    # tmp_dir = os.path.join('..', 'tmp')
    # Generate watermark qr_code
    qr_path = os.path.join(tmp_dir, 'watermark.svg')
    print_qr_code(qr_path)

    # Generate tex files
    rc_dirs = [os.path.join('..', 'resources'), os.path.join(args.input_dir), tmp_dir]

    # tex_printer = TexClassicPrinter(tmp_dir, rc_dirs)
    tex_printer = TexCardsPrinter(tmp_dir, rc_dirs)
    # tex_printer.paperSize = args.paper_size
    tex_printer.enableWatermark = args.watermark
    tex_printer.print_to(profile, 'main.tex')

    # Copy static resources
    for file in glob.glob(r'../resources/styles/*.*') + glob.glob(r'../resources/fonts/*.*'):
      shutil.copy(file, tmp_dir)

    # Compile PDF
    call_system('cd %s && xelatex %s main.tex %s' % (tmp_dir, ' '.join(LATEX_PARAMS), LATEX_OUTPUT))

    # Move result to output
    shutil.copy(os.path.join(tmp_dir, 'main.pdf'), os.path.join(out_dir, '%s_CV.pdf' % to_file_name(profile.personal['name'])))

    with LetterPrinter(tmp_dir, rc_dirs, 'cover_letter.tex') as printer:
      printer.print(profile)
    call_system('cd %s && xelatex %s cover_letter.tex %s' % (tmp_dir, ' '.join(LATEX_PARAMS), LATEX_OUTPUT))
    shutil.copy(os.path.join(tmp_dir, 'cover_letter.pdf'), os.path.join(out_dir, '%s_letter.pdf' % to_file_name(profile.personal['name'])))
    



if __name__ == "__main__":
    main()
