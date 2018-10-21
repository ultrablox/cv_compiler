#!/usr/local/bin/python3

import json
import datetime
import cairo
import cairo
import math
import urllib.parse
from enum import Enum, auto
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding

MAX_SCI_PUBS = 5
MAX_NON_SCI_PUBS = 3
MAX_CONFERENCES = 5
VISUAL_SKILL_COUNT = 22

def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)

def latex_protect(msg):
    msg = msg.replace('_', '\_')
    msg = msg.replace('%', '\%')
    msg = msg.replace('#', '\#')
    return msg

class TimePeriod:
    def __init__(self, data):
        interval = data.split('-')
        self.startDate = datetime.datetime.strptime(interval[0], '%d.%m.%Y')

        if interval[1] == 'now':
            self.endDate = datetime.datetime.now()
            self.isOpen = True
        else:
            self.endDate = datetime.datetime.strptime(interval[1], '%d.%m.%Y')
            self.isOpen = False


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
        self.parent = None
        
        self.period = TimePeriod(prj_node['period'])
        self.name = prj_node['name']

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
        self.totalExperience = 0

class Employment:
    def __init__(self, json_node, profile):
        self.name = json_node['name']
        self.period = TimePeriod(json_node['period'])
        self.web = json_node['web']
        self.role = json_node['role']
        self.description = json_node['description']
        self.notes = json_node['notes'] if 'notes' in json_node else [] 
        
        self.projects = []
        for prj in json_node['projects']:
            # print(prj)
            prj_ref = first_true(profile.projects, None, lambda p: p.name == prj)
            assert prj_ref != None
            prj_ref.parent = self
            self.projects += [prj_ref]


class EmployerProfile:
    def __init__(self):
        self.projects = []
        self.employments = []
    
    def deserialize(self, json_node):
        self.contacts = json_node['contacts']
        self.personal = json_node['personal']
        self.education = json_node['education']
        self.traits = json_node['traits']
    
        self.specialSkillGroups = json_node['special_skills']

        for prj in json_node["projects"]:       
            new_prj = Project(prj)
            self.projects += [new_prj]

        for employment_node in json_node['employments']:
            self.employments += [Employment(employment_node, self)]
        
        scopus_pubs = []
        other_pubs = []
        non_sci_pubs = []
        
        self.publicationStats = {}
        with open('blohin.bib') as bibtex_file:
            parser = BibTexParser()
            parser.customization = homogenize_latex_encoding
            bib_database = bibtexparser.load(bibtex_file, parser=parser)

            sorted_pubs = sorted(bib_database.entries, key=lambda pub: int(pub['year']), reverse=True)
            for publication in sorted_pubs:
                skip = False
                skip = skip or (('language' in publication) and (publication['language'] == 'russian'))
                skip = skip or (publication['ENTRYTYPE'] != 'article')

                if not skip:
                    if ('source' in publication) and (publication['source'] == 'Scopus'):
                        scopus_pubs += [publication]
                    else:
                        other_pubs += [publication]
            
            self.publicationStats['sci_total'] = len(bib_database.entries)
            self.publicationStats['scopus'] = len(scopus_pubs)

            if len(scopus_pubs) > MAX_SCI_PUBS:
                self.scientificPublications = scopus_pubs[0:MAX_SCI_PUBS]
            else:
                raise Exception('Not implemented')

        self.popularPublications = json_node['pop_publications'][0:MAX_NON_SCI_PUBS]

        self.conferences = json_node['conferences'][0:MAX_CONFERENCES]


    def init_skills(self, skills, skill_descriptions):
        # print(skill_descriptions)
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
        totals = totals[0:VISUAL_SKILL_COUNT]
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
        sorted_projects = sorted(self.projects, key=lambda prj: prj.period.startDate, reverse=True)

        with open("generated_projects.tex", "w") as file:
            for prj in sorted_projects:
                file.write("\project{%s}{%s}" % (latex_protect(prj.name), prj.icon))
                file.write("{%d-%s}" % (prj.period.startDate.year, 'present' if prj.period.isOpen else str(prj.period.endDate.year)))

                file.write("{}{%s}{" % (prj.description))

                first_line_items = []
                
                
                type_str = "$\\bullet$"
                if prj.parent:
                    type_str += " in %s" % prj.parent.name
                else:
                    type_str += " hobby"

                first_line_items += ["\\teamsize{%s}" % (prj.teamSize)]

                if prj.webLink:
                    url = urllib.parse.urlparse(prj.webLink)
                    label = url.netloc
                    if url.path:
                        label += url.path
                    first_line_items += ['\weblink{%s}{%s}' % (latex_protect(prj.webLink), latex_protect(label))]

                first_line_items += [type_str]
                
                file.write("\item %s\n" % ' '.join(first_line_items))

                file.write("\item \skills{%s}\n" % latex_protect(', '.join(prj.skills)))
                
                for achievement in prj.achievements:
                    file.write("\item \\achievement{%s}\n" % (latex_protect(achievement)))

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
                file.write("\job{%s}{%s}{%s}{%s}{%s}{%s}{\n" % (employment.period.startDate.strftime('%b %Y'), 'Present' if employment.period.isOpen else employment.period.endDate.strftime('%b %Y'), employment.name, employment.web, employment.role, employment.description))
                file.write("\t\\begin{itemize-noindent}\n")
                
                prj_names = []
                for prj in employment.projects:
                    prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_protect(prj.name))]

                notes_arr = ['\t\t\item{ worked in %s project%s}' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')]

                for note in employment.notes:
                    notes_arr += ['\t\t\item{%s}' % note]

                file.write("\n".join(notes_arr))
                file.write("\n")
                file.write("\t\end{itemize-noindent}\n")
                file.write("}\n")

    def generate_publications(self):
        with open("generated_scientific_publications.tex", "w") as file:
            file.write('(%d total, incl. %d Scopus)\n' % (self.publicationStats['sci_total'], self.publicationStats['scopus']))
            file.write('\\begin{itemize-noindent}\n')
            for publication in self.scientificPublications:
                file.write('\item %d --- %s // %s' % (int(publication['year']), publication['title'], publication['journal']))
                if ('source' in publication) and (publication['source'] == 'Scopus'):
                    file.write(' \scopus')
                file.write('\n')

            file.write('\end{itemize-noindent}\n')

    def generate_popular_publications(self):
        with open("generated_popular_publications.tex", "w") as file:
            
            file.write('\\begin{itemize-noindent}\n')
            for publication in self.popularPublications:
                file.write('\item \ppublication{%d}{%s}{%s}{%s}' % (publication['year'], publication['name'], publication['source'], latex_protect(publication['url'])))
            file.write('\end{itemize-noindent}\n')
        
    
    def generate_conferences(self):
        with open("generated_conferences.tex", "w") as file:
            conf_strs = []
            for conf in self.conferences:
                conf_strs += ['%s (%s, %d)' % (conf['name'], conf['location'], conf['year'])]
            file.write("%s, etc.\n" % ' '.join(conf_strs))

    def generate_educations(self):
        with open("generated_educations.tex", "w") as file:
            for edu in self.education:
                tp = TimePeriod(edu['period'])
                file.write('\education{%s}{%d-%d}{%s}{%s}{' % (edu['place'], tp.startDate.year, tp.endDate.year, edu['name'], latex_protect(edu['gpa'])))
                if ('notes' in edu) and (len(edu['notes']) > 0):
                    file.write('\\begin{itemize-noindent}')
                    notes_arr = []
                    for note in edu['notes']:
                        notes_arr += ['\item %s' % note]
                    file.write('\n'.join(notes_arr))
                    file.write('\end{itemize-noindent}')
                file.write('}')
    
    def generate_skills(self):
        totals = self.skillsArray.skills_totals()
        totals = totals[VISUAL_SKILL_COUNT:]

        skill_groups = {}
        #0, <1yr, 1-2yr, 2-5, 5-7, 7-10, 10+
        barriers = [0, 1, 2, 5, 7, 10, 1000]
        cur_gr_idx = 0
        with open("generated_skills.tex", "w") as file:
            for skill in totals:
                gr_val = 0
                for idx in range(0, len(barriers)):
                    if (barriers[idx] <= skill['size']) and (skill['size'] < barriers[idx+1]):
                        gr_val = barriers[idx]
                        break

                if gr_val in skill_groups:
                    skill_groups[gr_val] += [skill]
                else:
                    skill_groups[gr_val] = [skill]

            for barrier in reversed(barriers):
                if barrier in skill_groups:
                    barrier_idx = barriers.index(barrier)
                    group_name = '<1 year' if barrier_idx == 0 else '%d-%d years' % (barriers[barrier_idx], barriers[barrier_idx+1])
                    
                    skills = []
                    for sk in skill_groups[barrier]:
                        skills += [latex_protect(sk['name'])]
                    file.write('\\textbf{%s:} %s\n\n' % (group_name, ', '.join(skills)))

            for sgr in self.specialSkillGroups:
                file.write('\skillgroup{%s:}{%s}{\n' % (sgr['name'], sgr['details']))
                for adv in sgr['advantages']:
                    file.write('\item %s\n' % adv)
                file.write('}\n')

        # print(skill_groups)
    def generate_contacts(self):
        with open("personal_contacts.tex", "w") as file:
            file.write('Name: %s \splitter Sex: %s \splitter Date of birth: %s \splitter Nationality: %s \splitter %s \hfill \\break\n' % (self.personal['name'], self.personal['sex'], self.personal['birthdate'], self.personal['nationality'], self.personal['additional']))
            file.write('%s \hfill \\break\n' % self.contacts['residence'])
            file.write('\\vcenteredinclude{img/mail_logo.png} \href{mailto:%s}{%s}\n' % (self.contacts['email'], self.contacts['email']))
            file.write('\\vcenteredinclude{img/phone_logo.png} %s\n' % self.contacts['phone'])
            file.write('\\vcenteredinclude{img/linkedin_logo.png} \href{%s}{%s}\n' % (self.contacts['linkedin'], self.contacts['linkedin']))
            file.write('\\vcenteredinclude{img/skype_logo.png} %s \\\\\n' % self.contacts['skype'])
            file.write('\\textbf{Languages:} %s\n' % ', '.join(self.contacts['languages']))
    
    def generate_traits(self):
        with open("generated_traits.tex", "w") as file:
            for trait in self.traits:
                file.write('\item \\textbf{%s:} %s\n' % (trait['name'], trait['details']))

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
            min_date = min(min_date, new_prj.period.startDate)
        else:
            min_date = min(new_prj.period.startDate, new_prj.period.endDate)

        if max_date:
            max_date = max(max_date, new_prj.period.endDate)
        else:
            max_date = max(new_prj.period.startDate, new_prj.period.endDate)
    
    
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
            sa.fill(skill, di.index(new_prj.period.startDate), di.index(new_prj.period.endDate))

    # print("Your skills totals:")
    skills = sorted(skills, key=lambda rec: sa.skill_size(rec))


    for skill_name in profile.skills:
        profile.skills[skill_name].totalExperience = sa.skill_size(skill)
        # print("{0} - {1:0.1f} yrs.".format(skill, sa.skill_size(skill)))

    profile.skillsArray = sa
    profile.generate_skill_matrix()

    profile.generate_projects()
    profile.generate_employments()
    profile.generate_publications()
    profile.generate_conferences()
    profile.generate_popular_publications()
    profile.generate_educations()
    profile.generate_skills()
    profile.generate_contacts()
    profile.generate_traits()

if __name__ == "__main__":
    # execute only if run as a script
    main()