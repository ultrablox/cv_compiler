#!/usr/bin/env python3

from wizard import skill_extract_widget, profile_filter_widget, final_widget, letter_widget
import logging
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWizard
import sys
from db import skills_db
from letter import letter_project
import os
import argparse


def main():
  logging.basicConfig(level=logging.INFO)

  parser = argparse.ArgumentParser(description='Compile CV into PDF file.')
  parser.add_argument('--input_dir', type=str, default='../sample_input', help='input profile directory')
  args = parser.parse_args()


  # input_dir = os.path.abspath('../../my_cv/data')
  input_dir = args.input_dir
  letter_path = os.path.join(input_dir, 'letter.json')

  skills = skills_db.SkillsDB()
  skills.load_from_default_location()

  app = QtWidgets.QApplication(sys.argv)

  skills_widget = skill_extract_widget.SkillExtractWidget(skills)
  filter_widget = profile_filter_widget.ProfileFilterWidget(skills_widget, input_dir)
  letter_wdg = letter_widget.LetterWidget(letter_path, filter_widget)
  final_wdg = final_widget.FinalWidget(filter_widget, letter_wdg, input_dir)

  wizard = QWizard()
  wizard.addPage(skills_widget)
  wizard.addPage(filter_widget)
  wizard.addPage(letter_wdg)
  wizard.addPage(final_wdg)
  wizard.setWindowTitle('CV Assembler Wizzard')
  wizard.show()

  sys.exit(app.exec_())


if __name__ == "__main__":
    main()
