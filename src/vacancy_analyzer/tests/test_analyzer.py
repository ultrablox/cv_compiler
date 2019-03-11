import unittest
from vacancy_analyzer import analyzer
from db import skills_db


class TestStringMethods(unittest.TestCase):

  def test_simple_sentence(self):
    skills = skills_db.SkillsDB()
    skills.load_from_default_location()

    v_analyzer = analyzer.Analyzer(skills)
    v_analyzer.parse('You know C as well as C++, my little student.')
    self.assertEqual(v_analyzer.matched_names(), ['C', 'C++'])

