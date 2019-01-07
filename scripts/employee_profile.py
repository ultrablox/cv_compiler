
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from basic_entities import *
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding

MAX_SCI_PUBS = 4
MAX_NON_SCI_PUBS = 3
MAX_CONFERENCES = 5

class EmployeeProfile:
  def __init__(self):
    self.projects = []
    self.employments = []
    self.publicationStats = {}
    self.scientificPubs = []
    self.popularPubs = []

  def deserialize(self, json_node):
    self.contacts = json_node['contacts']
    self.personal = json_node['personal']
    self.education = json_node['education']
    self.traits = json_node['traits']

    self.specialSkillGroups = json_node['special_skills']

    # Deserialize projects
    for prj in json_node['projects']:
      self.projects += [Project(prj)]

    # Initialize full skill list
    self.skills = {}
    for name, data in json_node['skills'].items():
        self.skills[name] = Skill(name, data)

    for prj in self.projects:
      for skill_name in prj.get_total_skill_list():
        if skill_name not in self.skills:
          self.skills[skill_name] = Skill(skill_name)

    # Fill skill periods
    for prj in self.projects:
      log_print(LOG_LEVEL_DEBUG, 'Adding skill periods from project: %s' % prj.name)
      for prj_skill in prj.skills:
        self.skills[prj_skill].add_period(prj.period)

      for task in prj.tasks:
        for skill in task.skills:
          self.skills[skill].add_period(task.period)

    for employment_node in json_node['employments']:
        self.employments += [Employment(employment_node, self)]

    self.conferences = json_node['conferences'][0:MAX_CONFERENCES]

  def deserialize_publications(self, base_path):
    # Scientific publications
    sci_pubs_file = os.path.join(base_path, 'sci_publications.bib')
    if os.path.exists(sci_pubs_file):
      parser = BibTexParser()
      parser.customization = homogenize_latex_encoding
      with open(sci_pubs_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        self.scientificPubs = bib_database.entries
    # Popular publications
    pop_pubs_file = os.path.join(base_path, 'pop_publications.bib')
    if os.path.exists(pop_pubs_file):
      parser = BibTexParser()
      parser.customization = homogenize_latex_encoding
      with open(pop_pubs_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        self.popularPubs = bib_database.entries

  # Returns array [{'name' : 'skill_name', 'size' : .f_years}]
  def skills_totals(self):
    res = []
    for key, data in self.skills.items():
        res += [{'name': data.name_with_abbr(), 'size': data.total_size(), 'attitude': data.attitude}]
    res = (item for item in res if item['size'] > 0.0)
    return sorted(res, key=lambda rec: rec['size'], reverse=True)

  # def add_period_for_skill(self, skill, period):
  #     if not skill in self.skills:
  #         new_skill = Skill(skill)
  #         self.skills[skill] = new_skill
  #     cur_skill = self.skills[skill]
  #     cur_skill.add_period(period)

  def best_skill(self):
      skills = self.skills_totals()
      return skills[0]['size']

  def has_activities(self):
    return self.popularPubs or self.scientificPubs or self.conferences

  def scopus_publication_count(self):
    return sum(is_scopus(pub) for pub in self.scientificPubs)

  # Marks most important publication as visible
  def compress(self):
    ###
    ### Scientific publications
    ###
    # Only articles are printed
    # Scopus have priority over simple publication

    good_count = 0
    for pub in self.scientificPubs:
      skip = False
      skip = skip or (('language' in pub) and (pub['language'] == 'russian'))
      skip = skip or (pub['ENTRYTYPE'] != 'article')
      pub['visible'] = not skip

      if not skip:
        good_count += 1

    # Check if we can print all of them 
    if good_count > MAX_SCI_PUBS:
      # Sort so good are first
      self.scientificPubs = sorted(self.scientificPubs, key=lambda pub: pub['visible'], reverse=True)


      # Sort leftmost by scopus
      self.scientificPubs[0:good_count] = sorted(self.scientificPubs[0:good_count], key=lambda pub: int(is_scopus(pub)), reverse=True)

      # Sort both subsets by year
      scopus_count = 0
      for pub in self.scientificPubs[0:good_count]:
        if is_scopus(pub):
          scopus_count += 1
      log_print(LOG_LEVEL_DEBUG, 'Total scopus publications: %d' % scopus_count)



      self.scientificPubs[0:scopus_count] = sorted(self.scientificPubs[0:scopus_count], key=lambda pub: int(pub['year']), reverse=True)
      # print(self.scientificPubs[0:good_count])
      # exit(1)

      self.scientificPubs[scopus_count:good_count] = sorted(self.scientificPubs[scopus_count:good_count], key=lambda pub: int(pub['year']), reverse=True)

      # print(self.scientificPubs[0:good_count])

      # Mark invisible all that exceed the number
      for i in range(MAX_SCI_PUBS, good_count):
        self.scientificPubs[i]['visible'] = False

    # After all manipulation sort in year order for further printing
    self.scientificPubs = sorted(self.scientificPubs, key=lambda pub: int(pub['year']), reverse=True)

    ###
    ### Popular publications
    ###
    # They have the same priority - simply cut off tail
    self.popularPubs = sorted(self.popularPubs, key=lambda pub: int(pub['year']), reverse=True)

    for i in range(0, len(self.popularPubs)):
      pub = self.popularPubs[i]
      pub['visible'] = (i < MAX_NON_SCI_PUBS)

