import cairo
import math
from skill_attitude import *

VISUAL_SKILL_COUNT = 22

class SkillMatrix:
  def __init__(self, employer_profile):
    self.maxValue = employer_profile.best_skill()
    self.totals = employer_profile.skills_totals()
    self.skills = employer_profile.skills

  def compile(self, out_path):
    surface = cairo.PDFSurface(out_path, 600, 325)
    cr = cairo.Context(surface)
    cr.save()

    # snippet.draw_func(cr, width, height)

    # cr.scale(width, height)
    cr.set_line_width(1.0)

    
    cr.set_font_size(14)


    # totals = self.skills_totals()
    totals = self.totals[0:VISUAL_SKILL_COUNT]
    # print(totals)
    
    PIVOT_X = 0.0
    PIVOT_Y = 230.0
    graph_height = 200
    graph_width = 570
    
    #Annotate axis
    cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.save()
    cr.move_to(PIVOT_X + 20, PIVOT_Y - graph_height / 2 + 70)
    cr.rotate(-math.pi/2)
    cr.show_text("Experience, yrs.")
    cr.restore()

    #Annotate attitudes
    cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    

    labels = ['Positive', 'Neutral', 'Negative']
    colors = [cairo.SolidPattern(0.0, 1.0, 0.0), cairo.SolidPattern(0.8, 0.8, 0.8), cairo.SolidPattern(1.0, 0.0, 0.0)]
    for i in range(0, 3):
      cr.save()

      cr.rectangle(PIVOT_X + graph_width - 25, 30 -15 + 25*i, 20, 20)
      cr.set_source(colors[i])
      cr.fill()

      extents = cr.text_extents(labels[i]);
      
      cr.set_source_rgba(0, 0, 0, 1.0);
      cr.move_to(PIVOT_X + graph_width - 30 - extents.width - extents.x_bearing, 30 + 25*i)
      cr.show_text(labels[i])

      cr.restore()
    
    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    idx = 1
    for skill in totals:
      #Annotate skill
      cr.save()
      cr.move_to(PIVOT_X + idx * 25.0, PIVOT_Y)
      cr.rotate(math.pi/4)
      cr.show_text(skill['name'])
      cr.restore()

      #Draw it's value
      value_h = graph_height * skill['size'] / self.maxValue

      cr.save()
      # print(skill['size'])
      cr.move_to(PIVOT_X + idx * 25.0, PIVOT_Y)
      cr.set_line_width(1.0)
      cr.rectangle(PIVOT_X + idx * 25.0, PIVOT_Y - 10.0, 20.0, - value_h)

      switcher = {
          SkillAttitude.FAVOURITE: colors[0],
          SkillAttitude.NEUTRAL: colors[1],
          SkillAttitude.NEGATIVE: colors[2]
      }
      
      color_func = switcher.get(self.skills[skill['name']].attitude, lambda: cairo.SolidPattern(1.0, 0.0, 0.0))

      cr.set_source(color_func)
      cr.fill()
      cr.restore()

      #Annotte value
      cr.save()
      cr.move_to(PIVOT_X + idx * 25.0, PIVOT_Y - value_h - 14)#

      fmt = '%.0f' if skill['size'] > 10.0 else '%.1f'
      cr.show_text(fmt % skill['size'])
      cr.restore()

      idx += 1

    cr.restore()
    cr.show_page()
    surface.finish()
