
import math
from skill_attitude import *
from utils import *

VISUAL_SKILL_COUNT = 22

class SkillMatrix:
  def __init__(self, employer_profile):
    self.maxValue = employer_profile.best_skill()
    self.totals = employer_profile.skills_totals()
    self.skills = employer_profile.skills

  def generate(self, file):
    # They are already sorted
    top_skills = self.totals[0:VISUAL_SKILL_COUNT]
    
    coords = [x['name'] for x in top_skills]
    

    file.writelines(['\pgfplotsset{compat=1.8}\n',
      '\\begin{tikzpicture}\n',
      '\\begin{axis}[\n',
      '\tybar stacked,\n',
      '\tbar width=12pt,\n',
      '\taxis lines=middle,\n',
      '\ty label style={at={(axis description cs:-0.025,.5)},rotate=90,anchor=south},\n',
      '\tylabel={Experience, years},\n',
      '\tsymbolic x coords={%s},\n' % latex_escape(','.join(coords)),
      '\txtick=data,\n',
      '\tytick=\empty,\n',
      '\tx tick label style={rotate=45,anchor=east,align=center},\n',
      '\taxis x line=bottom,\n',
      '\taxis y line=left,\n',
      '\tenlargelimits=false,\n',
      '\tclip=false,\n'
      '\twidth=0.75\\textwidth,\n'
      '\theight=8cm\n'
      ']\n'])
  
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['green', 'gray', 'orange']

    vals = [[0] * VISUAL_SKILL_COUNT, [0] * VISUAL_SKILL_COUNT, [0] * VISUAL_SKILL_COUNT]
  
    switcher = {
        SkillAttitude.FAVOURITE: 0,
        SkillAttitude.NEUTRAL: 1,
        SkillAttitude.NEGATIVE: 2
    }

    for i in range(0, VISUAL_SKILL_COUNT):
      cur_skill = top_skills[i]
      att = self.skills[cur_skill['name']].attitude
      idx = switcher.get(att, 0)
      vals[idx][i] = cur_skill['size']

    for i in range(0, 3):
      x_coords = [''] * VISUAL_SKILL_COUNT
      for j in range(0, VISUAL_SKILL_COUNT):
        x_coords[j] = '(%s,%.1f)' % (top_skills[j]['name'], vals[i][j])
      # vals = []
      format_str = ', nodes near coords*' if (i == 2) else ''
      file.write('\\addplot[fill=%s%s] coordinates {%s};\n' % (colors[i], format_str, latex_escape(' '.join(x_coords))))
      file.write('\\addlegendentry{%s}\n' % labels[i])
    
    file.writelines(['\end{axis}\n',
      '\end{tikzpicture}\n',
      '\\newline\n'])
