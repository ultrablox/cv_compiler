#!/usr/local/bin/python3

import json
import datetime
import cairo
import cairo
import math
import urllib.parse
from enum import Enum, auto

def latex_protect(msg):
    msg = msg.replace('_', '\_')
    msg = msg.replace('%', '\%')
    msg = msg.replace('#', '\#')
    return msg

class DateIndexer:
    def __init__(self, min_date, max_date):
        self.minDate = min_date
        self.maxDate = max_date
    
    def month_count(self):
        return self.index(self.maxDate)

    def index(self, date):
        return (date.year - self.minDate.year) * 12 + (date.month - self.minDate.month)

class SkillsArray:
    def __init__(self, skills, months):
        self.skillUsage = {}
        for skill in skills:
            self.skillUsage[skill] = [0] * months
        
    def fill(self, skill, first, last):
        for idx in range(first, last):
            # print(idx)
            self.skillUsage[skill][idx] = 1
    
    def skill_size(self, skill):
        skill_arr = self.skillUsage[skill]
        return sum(1 for item in skill_arr if item==(1)) / 12.0

    def skills_totals(self):
        res = []
        for key, usage in self.skillUsage.items():
            res += [{"name" : key, "size" : self.skill_size(key)}]
            # res[key] = 
        return sorted(res, key=lambda rec: -self.skill_size(rec["name"]))

    def best_skill(self):
        skills = self.skills_totals()
        return skills[0]['size']

class SkillAttitude(Enum):
    FAVOURITE = auto()
    NEUTRAL = auto()
    NEGATIVE = auto()

class Project:
    def __init__(self, prj_node):
        self.name = prj_node['name']
        interval = prj_node['period'].split('-')
        self.startDate = datetime.datetime.strptime(interval[0], '%d.%m.%Y')

        if interval[1] == 'now':
            self.endDate = datetime.datetime.now()
            self.isCurrent = True
        else:
            self.endDate = datetime.datetime.strptime(interval[1], '%d.%m.%Y')
            self.isCurrent = False

        self.icon = ''
        if 'icon' in prj_node:
            self.icon = prj_node['icon']

        self.description = prj_node['description']
        if 'web' in prj_node:
            self.webLink = prj_node['web']
        else:
            self.webLink = None

        self.teamSize = prj_node['team-size']

        self.achievements = []
        if 'achievements' in prj_node:
            self.achievements = prj_node['achievements']

        self.skills = []

        for skill in prj_node['skills']:
            self.skills += [skill]

        self.notes =[]
        if 'notes' in prj_node:
            self.notes += [prj_node['notes']]


class Skill:
    def __init__(self, name):
        self.name = name
        self.attitude = SkillAttitude.NEUTRAL

class Employment:
    def __init__(self, json_node):
        self.name = json_node['name']
        self.web = json_node['web']
        self.role = json_node['role']
        self.description = json_node['description']


class EmployerProfile:
    def __init__(self):
        self.projects = []
        self.employments = []
    
    def deserialize(self, json_node):
        for employment_node in json_node['employments']:
            self.employments += [Employment(employment_node)]

    def init_skills(self, skills, skill_descriptions):
        print(skill_descriptions)
        self.skills = {}

        for skill in skills:
            new_skill = Skill(skill)
            if skill in skill_descriptions:
                sd = skill_descriptions[skill]

                if 'attitude' in sd:
                    switcher = {
                        'favourite' : SkillAttitude.FAVOURITE,
                        'neutral' : SkillAttitude.NEUTRAL,
                        'negative' : SkillAttitude.NEGATIVE
                    }
                    new_skill.attitude = switcher.get(sd['attitude'], lambda: None)            
            self.skills[skill] = new_skill
                # print(sd)


    def generate_skill_matrix(self):
        surface = cairo.PDFSurface("skill_matrix.pdf", 600, 300)
        cr = cairo.Context(surface)
        cr.save()

        # snippet.draw_func(cr, width, height)

        # cr.scale(width, height)
        cr.set_line_width(1.0)

        
        cr.set_font_size(14)
        
        max_value = self.skillsArray.best_skill()
        # print(max_value)

        totals = self.skillsArray.skills_totals()
        # print(totals)
        
        PIVOT_X = 0.0
        PIVOT_Y = 230.0
        graph_height = 200
    
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.save()
        cr.move_to(PIVOT_X + 20, PIVOT_Y - graph_height / 2 + 70)
        cr.rotate(-math.pi/2)
        cr.show_text("Experience, yrs.")
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
            value_h = graph_height * skill['size'] / max_value

            cr.save()
            # print(skill['size'])
            cr.move_to(PIVOT_X + idx * 25.0, PIVOT_Y)
            cr.set_line_width(1.0)
            cr.rectangle(PIVOT_X + idx * 25.0, PIVOT_Y - 10.0, 20.0, - value_h)

            switcher = {
                SkillAttitude.FAVOURITE: cairo.SolidPattern(0.0, 1.0, 0.0),
                SkillAttitude.NEUTRAL: cairo.SolidPattern(0.8, 0.8, 0.8),
                SkillAttitude.NEGATIVE: cairo.SolidPattern(1.0, 0.0, 0.0)
            }
            
            color_func = switcher.get(self.skills[skill['name']].attitude, lambda: cairo.SolidPattern(1.0, 0.0, 0.0))

            cr.set_source(color_func)
            cr.fill()
            cr.restore()

            #Annotte value
            cr.save()
            cr.move_to(PIVOT_X + idx * 25.0, PIVOT_Y - value_h)

            fmt = '%.0f' if skill['size'] > 10.0 else '%.1f'
            cr.show_text(fmt % skill['size'])
            cr.restore()

            idx += 1

        #Annotate years
        # idx = 1
        # while idx < max_value:
        #     cr.save()
        #     cr.move_to(PIVOT_X, PIVOT_Y - graph_height * idx / max_value)
        #     cr.show_text(str(idx))
        #     cr.restore()
        #     idx += 1
        #     # print(idx)


        cr.restore()
        cr.show_page()
        surface.finish()
    
    def generate_projects(self):
        sorted_projects = sorted(self.projects, key=lambda prj: prj.startDate, reverse=True)

        with open("generated_projects.tex", "w") as file:
            for prj in sorted_projects:
                file.write("\project{%s}{%s}" % (latex_protect(prj.name), prj.icon))
                file.write("{%d-%s}" % (prj.startDate.year, 'present' if prj.isCurrent else str(prj.endDate.year)))
                file.write("{hobby}{%s}{" % (prj.description))

                first_line_items = []
                first_line_items += ["\\teamsize{%s}" % (prj.teamSize)]

                if prj.webLink:
                    url = urllib.parse.urlparse(prj.webLink)
                    label = url.netloc
                    if url.path:
                        label += url.path
                    first_line_items += ['\weblink{%s}{%s}' % (latex_protect(prj.webLink), latex_protect(label))]

                
                file.write("\item %s\n" % ' '.join(first_line_items))
                
                for achievement in prj.achievements:
                    file.write("\item \\achievement{%s}\n" % (latex_protect(achievement)))
                
                file.write("\item \skills{%s}\n" % latex_protect(', '.join(prj.skills)))

                if len(prj.notes) != 0:
                    file.write("\item %s\n" % latex_protect('; '.join(prj.notes)))

                file.write("}{charon:project}\n" )
    #     \item \weblink{http://ultraoutliner.com}{http://ultraoutliner.com}
    #     \item skills: C++, QT, Ruby on Rails, Javascript, fullstack, Agile, marketing, CEO
    #     \item achievement: alone with no investments implemented idea into software, promoted it, attracted audience, partners and contributors
    #     \item effect: got 1000+ active users total, 150-200 unique site visitors/week
    # }{outliner:project}")
        # file.write("Your text goes here") 
    #     \project{ultra\_outliner}{outliner_project.png}{2016-present}{hobby}{Card-based outlining software for screenwriters and storytellers}{
    #     \item \weblink{http://ultraoutliner.com}{http://ultraoutliner.com}
    #     \item skills: C++, QT, Ruby on Rails, Javascript, fullstack, Agile, marketing, CEO
    #     \item achievement: alone with no investments implemented idea into software, promoted it, attracted audience, partners and contributors
    #     \item effect: got 1000+ active users total, 150-200 unique site visitors/week
    # }{outliner:project}
    def generate_employments(self):
        with open("generated_employments.tex", "w") as file:
            for employment in self.employments:
                file.write("\job{Sept 2018}{Present}{%s}{%s}{%s}{%s}{" % (employment.name, employment.web, employment.role, employment.description))
                file.write("\\begin{itemize-noindent}")
                file.write("\item{worked }")
                file.write("\end{itemize-noindent}")
                file.write("}\n")

def main():
    data = {}

    with open('data.json', 'r') as json_data:
        data = json.load(json_data)
    # print(data["skills"])

    profile = EmployerProfile()
    profile.deserialize(data)

    #Initialize skills
    skills = []

    # Run along the projects and look for the minmal and maximum date
    min_date = None
    max_date = None
    for prj in data["projects"]:
        for skill in prj["skills"]:
            skills.append(skill)
        
        new_prj = Project(prj)

        if min_date:
            min_date = min(min_date, new_prj.startDate)
        else:
            min_date = min(new_prj.startDate, new_prj.endDate)

        if max_date:
            max_date = max(max_date, new_prj.endDate)
        else:
            max_date = max(new_prj.startDate, new_prj.endDate)
    
    
    print("Your employment history is {0} - {1}".format(min_date, max_date))

    skills = list(set(skills))
    profile.init_skills(skills, data['skills'])

    print("Total set of skills: {0}".format(skills))
    
    di = DateIndexer(min_date, max_date)

    # Calculate the array size for the whole time periods
    # Create the array and fill it with zeros
    sa = SkillsArray(skills, di.month_count())

    # Iterate all the projects
    for prj in data["projects"]:
        # Find mim and max index for the time period
        new_prj = Project(prj)

        # Foreach skill
        for skill in prj["skills"]:
            # Fill as 'used' along the time period
            sa.fill(skill, di.index(new_prj.startDate), di.index(new_prj.endDate))

        profile.projects += [new_prj]

    # print("Your skills totals:")
    skills = sorted(skills, key=lambda rec: sa.skill_size(rec))
    
    # for skill in skills:
    #     print("{0} - {1:0.1f} yrs.".format(skill, sa.skill_size(skill)))

    profile.skillsArray = sa
    profile.generate_skill_matrix()

    profile.generate_projects()
    profile.generate_employments()

if __name__ == "__main__":
    # execute only if run as a script
    main()