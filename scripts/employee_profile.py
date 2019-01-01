from basic_entities import *
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding

MAX_SCI_PUBS = 5
MAX_NON_SCI_PUBS = 3
MAX_CONFERENCES = 5

class EmployeeProfile:
  def __init__(self):
      self.projects = []
      self.employments = []
      self.publicationStats = {}
  
  def deserialize(self, json_node):
      self.contacts = json_node['contacts']
      self.personal = json_node['personal']
      self.education = json_node['education']
      self.traits = json_node['traits']
  
      self.specialSkillGroups = json_node['special_skills']
      
      self.skills = {}

      for skill in json_node['skills']:
          new_skill = Skill(skill)
          sd = json_node['skills'][skill]
          if 'attitude' in sd:
              switcher = {
                  'favourite' : SkillAttitude.FAVOURITE,
                  'neutral' : SkillAttitude.NEUTRAL,
                  'negative' : SkillAttitude.NEGATIVE
              }
              new_skill.attitude = switcher.get(sd['attitude'], lambda: None)
          self.skills[skill] = new_skill

      for prj in json_node['projects']:
          new_prj = Project(prj)
          self.projects += [new_prj]
          
          if 'skills' in prj:
              for prj_skill in prj['skills']:
                  self.add_period_for_skill(prj_skill, new_prj.period)

          if 'secondary_skills' in prj:
              for sec_skill in prj['secondary_skills']:
                  self.add_period_for_skill(sec_skill['name'], TimePeriod(sec_skill['period']))
      
      # Remove empty skills
      empty_skills = []
      for skill_name, skill_data in self.skills.items():
          if skill_data.total_size() == 0.0:
              empty_skills += [skill_name]

      for empty_name in empty_skills:
          del self.skills[empty_name]

      for employment_node in json_node['employments']:
          self.employments += [Employment(employment_node, self)]
      
      # non_sci_pubs = []

      # self.popularPublications = json_node['pop_publications'][0:MAX_NON_SCI_PUBS]

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
    else:
      self.scientificPubs = None

    # Popular publications
    pop_pubs_file = os.path.join(base_path, 'pop_publications.bib')
    if os.path.exists(pop_pubs_file):
      parser = BibTexParser()
      parser.customization = homogenize_latex_encoding
      with open(pop_pubs_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        self.popularPubs = bib_database.entries
    else:
      self.popularPubs = None

  
  def skills_totals(self):
      res = []
      for key, data in self.skills.items():
          res += [{'name' : key, 'size' : data.total_size()}]
      return sorted(res, key=lambda rec: rec['size'], reverse=True)

  def add_period_for_skill(self, skill, period):
      if not skill in self.skills:
          new_skill = Skill(skill)
          self.skills[skill] = new_skill
      cur_skill = self.skills[skill]
      cur_skill.add_period(period)
  
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
      self.scientificPubs[0:good_count] = sorted(self.scientificPubs[0:good_count], key=lambda pub: is_scopus(pub), reverse=True)

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
      
