
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


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
    visual_count = min(len(self.totals), VISUAL_SKILL_COUNT)
    top_skills = self.totals[0:visual_count]
    
    coords = [x['name'] for x in top_skills]
    
    file.writelines(['\pgfplotsset{\n',
      'compat=1.8,\n',
      # 'tick label style = {font=Arial Narrow},\n',
      # 'every axis label = {font=Arial Narrow},\n',
      # 'legend style = {font=Arial Narrow},\n',
      # 'label style = {font=Arial Narrow}\n',
      # 'node style = {}\n',
      'every non boxed x axis/.append style={x axis line style=-},',
      'every non boxed y axis/.append style={y axis line style=-}',
      '}\n'
    ])

    file.writelines(['\\begin{tikzpicture}\n',
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
      # 'enlarge y limits=0.03,\n',
      '\tclip=false,\n'
      '\twidth=0.75\\textwidth,\n'
      '\theight=6cm,\n',
      'every node near coord/.append style={font=\\bfseries, /pgf/number format/.cd, fixed, fixed zerofill, precision=1},\n'
      ']\n'])
  
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['green', 'gray', 'orange']

    vals = [[0] * visual_count, [0] * visual_count, [0] * visual_count]
  
    switcher = {
        SkillAttitude.FAVOURITE: 0,
        SkillAttitude.NEUTRAL: 1,
        SkillAttitude.NEGATIVE: 2
    }

    for i in range(0, visual_count):
      cur_skill = top_skills[i]
      att = cur_skill['attitude']
      idx = switcher.get(att, 0)
      vals[idx][i] = cur_skill['size']

    for i in range(0, 3):
      x_coords = [''] * visual_count
      for j in range(0, visual_count):
        x_coords[j] = '(%s,%f)' % (top_skills[j]['name'], vals[i][j])
      # vals = []
      format_str = ', nodes near coords*' if (i == 2) else ''
      file.write('\\addplot[fill=%s%s, draw=none] coordinates {%s};\n' % (colors[i], format_str, latex_escape(' '.join(x_coords))))
      file.write('\\addlegendentry{%s}\n' % labels[i])
    
    file.writelines(['\end{axis}\n',
      '\end{tikzpicture}\n',
      '\\newline\n'])
