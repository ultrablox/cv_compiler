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
      

      self.popularPublications = json_node['pop_publications'][0:MAX_NON_SCI_PUBS]

      self.conferences = json_node['conferences'][0:MAX_CONFERENCES]

  def deserialize_publications(self, pubs_path):
    scopus_pubs = []
    other_pubs = []
    
    with open(pubs_path, encoding='utf-8') as bibtex_file:
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