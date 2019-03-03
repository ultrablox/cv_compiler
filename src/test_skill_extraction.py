

import unittest
import glob

from utils import *


class TestStringMethods(unittest.TestCase):

  def test_skill_extraction(self):
    data_dir = os.path.join('..', 'test_data')

    vacancy_files = os.path.join(data_dir, 'vacancy.*.txt')
    for vacancy_file in glob.glob(vacancy_files):
      tmp_file_name = 'skills_tmp.txt'
      call_system('./extract_skills.py {} > {}'.format(vacancy_file, tmp_file_name))
      correct_skills_file = '{}.skills'.format(vacancy_file)

      extracted_skills = load_skills(tmp_file_name)
      correct_skills = load_skills(correct_skills_file)

      # print(extracted_skills)
      # print(correct_skills)
      self.assertEqual(extracted_skills, correct_skills)
    # self.assertEqual('foo'.upper(), 'FOO')