#!/usr/bin/env python3

from skill_attitude import *
import json
import datetime

import urllib.parse
import sys, os
import argparse
from check import *
from skill_matrix import *
from basic_entities import *
import glob
import shutil
from tex_printer import *
from employee_profile import *

DEBUG_LATEX = False

LATEX_OUTPUT = '' if DEBUG_LATEX else '1>/dev/null'
LATEX_PARAMS = [] if DEBUG_LATEX else ['-halt-on-error', '--interaction=batchmode']
        

def main():
  parser = argparse.ArgumentParser(description='Compile CV into PDF file.')
  parser.add_argument('--input_dir', type=str, default='/input', help='Input directory')
  parser.add_argument('--tmp_dir', type=str, default='/tmp', help='Temporary directory')
  parser.add_argument('--out_dir', type=str, default='/out', help='Output directory')
  parser.add_argument('--paper_size', type=str, default='a4', choices=['a4', 'a5'], help='Paper size')
  args = parser.parse_args()

  # Check necessary paths exist 
  check_always(os.path.exists(args.input_dir), 'Input directory "%s" does not exist' % args.input_dir)
  check_always(os.path.exists(args.tmp_dir), 'Temp directory "%s" does not exist' % args.tmp_dir)
  check_always(os.path.exists(args.out_dir), 'Output directory "%s" does not exist' % args.out_dir)

  # Check input structure
  data_path = os.path.join(args.input_dir, 'data.json')
  check_always(os.path.exists(data_path), 'Primary input "%s" does not exist' % data_path)

  lead_path = os.path.join(args.input_dir, 'lead.txt')
  check_always(os.path.exists(lead_path), 'Lead text "%s" does not exist' % lead_path)
  # shutil.copy(lead_path, os.path.join(args.tmp_dir, 'lead.tex'))
  
  # Load input data
  profile = EmployeeProfile()
  with open(data_path, 'r') as json_data:
      data = json.load(json_data)
      profile.deserialize(data)

  with open(lead_path, 'r') as file:
    profile.lead = file.read()

  profile.deserialize_publications(args.input_dir)
  profile.compress()
  
  # Generate tex files
  rc_dirs = [os.path.join('..', 'resources'), os.path.join(args.input_dir)]
  
  tex_printer = TexCVPrinter(args.tmp_dir, rc_dirs)
  tex_printer.paperSize = args.paper_size
  tex_printer.print_to(profile, 'main.tex')

  # Copy static resources
  for file in glob.glob(r'../resources/styles/*.*') + glob.glob(r'../resources/fonts/*.*'):
    shutil.copy(file, args.tmp_dir)

  # Compile PDF
  call_system('cd %s && xelatex %s main.tex %s' % (args.tmp_dir, ' '.join(LATEX_PARAMS), LATEX_OUTPUT))

  # Move result to output
  shutil.copy(os.path.join(args.tmp_dir, 'main.pdf'), os.path.join(args.out_dir, '%s_CV.pdf' % to_file_name(profile.personal['name'])))

if __name__ == "__main__":
    main()
