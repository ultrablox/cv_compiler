
# python3 -m unittest discover

import unittest
import glob
import tempfile
from db import skills_db


class TestStringMethods(unittest.TestCase):

  def test_unconnected_nodes(self):
    db_obj = skills_db.SkillsDB()
    self.assertEqual(db_obj.graph.number_of_nodes(), 1) # Only matcher

    for skill in ['C++', 'C#', 'C']:
      db_obj.create_skill(skill)

    self.assertEqual(db_obj.graph.number_of_nodes(), 4)

  def test_duplicated_nodes(self):
    db_obj = skills_db.SkillsDB()
    self.assertEqual(db_obj.graph.number_of_nodes(), 1) # Only matcher

    for skill in ['C++', 'C#', 'C', 'C++', 'C#', 'C#']:
      db_obj.create_skill(skill)

    self.assertEqual(db_obj.graph.number_of_nodes(), 4)
