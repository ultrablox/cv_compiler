import unittest
from vacancy_analyzer import analyzer


class TestStringMethods(unittest.TestCase):

  def test_simple_sentence(self):
    v_analyzer = analyzer.Analyzer()
    v_analyzer.parse('You know C as well as C++, my little student.')
    self.assertEqual(v_analyzer.matched_names(), ['C', 'C++'])

