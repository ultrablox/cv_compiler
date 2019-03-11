import unittest
# from letter import compiler
from letter import letter_project


class TestStringMethods(unittest.TestCase):

  def test_simple_letter(self):
    letter = letter_project.LetterProject()

    # letter.create_intro_section('Bruce Wayne', 'Batman Of the City')
    # letter.create_conclusion_section()
    letter.deserialize('../sample_input/letter.json')



    # v_analyzer = analyzer.Analyzer()
    # v_analyzer.parse('You know C as well as C++, my little student.')
    # self.assertEqual(v_analyzer.matched_names(), ['C', 'C++'])

