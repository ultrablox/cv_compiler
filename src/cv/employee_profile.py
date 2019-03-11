
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

import os
from cv.project import *
from cv.employment import *
from cv.skill_experience import *
# from cv.task import *
import bibtexparser
import json
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import homogenize_latex_encoding
import logging
from bibtexparser.bibdatabase import BibDatabase
import shutil

MAX_SCI_PUBS = 3
MAX_NON_SCI_PUBS = 3
MAX_CONFERENCES = 2


class EmployeeProfile:
  def __init__(self, skill_db):
    self.projects = []
    self.employments = []
    self.publicationStats = {}
    self.scientificPubs = []
    self.popularPubs = []
    self.skillDb = skill_db
    self.skillRecords = []
    self.traits = []
    self.specialSkillGroups = []
    self.conferences = []
    self.__total_employment = None

  def load(self, input_dir):
    # Check input structure
    data_path = os.path.join(input_dir, 'data.json')
    assert os.path.exists(data_path), 'Primary input "%s" does not exist' % data_path

    lead_path = os.path.join(input_dir, 'lead.txt')
    assert os.path.exists(lead_path), 'Lead text "%s" does not exist' % lead_path

    with open(data_path, 'r') as json_data:
      data = json.load(json_data)
      self.deserialize_data(data)

    with open(lead_path, 'r') as file:
      self.lead = file.read()

    self.deserialize_publications(input_dir)

  def serialize_data(self, json_node):
    json_node['contacts'] = self.contacts
    json_node['personal'] = self.personal
    json_node['education'] = self.education
    json_node['traits'] = self.traits

  def deserialize_data(self, json_node):
    self.contacts = json_node['contacts']
    self.personal = json_node['personal']
    self.education = json_node['education']
    if 'traits' in json_node:
      self.traits = json_node['traits']

    if 'special_skills' in json_node:
      self.specialSkillGroups = json_node['special_skills']

    # Deserialize projects
    prj_id = 1
    for prj in json_node['projects']:
      new_prj = Project()
      new_prj.deserialize(prj, self)
      new_prj.id = prj_id
      self.projects += [new_prj]
      prj_id += 1

    # Initialize full skill list
    project_skills = []
    for prj in self.projects:
      project_skills += prj.get_total_skill_list()

    if 'preferences' in json_node:
      project_skills = list(set(project_skills))
      preferences = json_node['preferences']
      pref_switcher = {
          'favourite': SkillAttitude.FAVOURITE,
          'neutral': SkillAttitude.NEUTRAL,
          'negative': SkillAttitude.NEGATIVE
      }

      for skill_name in project_skills:
        pref_str = preferences[skill_name] if skill_name in preferences else 'neutral'
        skill_att = pref_switcher.get(pref_str, SkillAttitude.NEUTRAL)

        skill_ref = self.skillDb.find_skill(skill_name)
        if not skill_ref:
          logging.warning('Unkown skill found: %s' % skill_name)
          skill_ref = self.skillDb.create_skill(skill_name)

        skill_rec = SkillExperience(skill_ref)
        skill_rec.attitude = skill_att
        self.skillRecords += [skill_rec]
    else:
      assert 'skills' in json_node, 'Strange JSON, where did you get it?'
      for skill_node in json_node['skills']:
        skill_ref = self.skillDb.find_skill(skill_node['name'], True)
        skill_rec = SkillExperience(skill_ref)
        skill_rec.deserialize(skill_node)

        self.skillRecords += [skill_rec]

    # Fill skill periods
    for prj in self.projects:
      for task in prj.tasks:
        for skill in task.skills:
          self.add_skill_experience(skill, task.period)

    emp_idx = 0
    for employment_node in json_node['employments']:
      new_empl = Employment()
      new_empl.deserialize(employment_node, self)
      new_empl.id = emp_idx
      self.employments += [new_empl]
      emp_idx += 1

    if 'conferences' in json_node:
      self.conferences = json_node['conferences']

    if 'total_employment' in json_node:
      self.__total_employment = TimePeriod(json_node['total_employment'])
    else:
      self.__total_employment = self.total_employment()

  def deserialize_publications(self, base_path):
    # Scientific publications
    self.__sci_pubs_file = os.path.join(base_path, 'sci_publications.bib')
    if os.path.exists(self.__sci_pubs_file):
      parser = BibTexParser()
      parser.customization = homogenize_latex_encoding
      with open(self.__sci_pubs_file, encoding='utf-8') as bibtex_file:
        self.__sci_bib_database = bibtexparser.load(bibtex_file, parser=parser)
        self.scientificPubs = self.__sci_bib_database.entries
    # Popular publications
    self.__pop_pubs_file = os.path.join(base_path, 'pop_publications.bib')
    if os.path.exists(self.__pop_pubs_file):
      parser = BibTexParser()
      parser.customization = homogenize_latex_encoding
      with open(self.__pop_pubs_file, encoding='utf-8') as bibtex_file:
        self.__pop_bib_database = bibtexparser.load(bibtex_file, parser=parser)
        self.popularPubs = self.__pop_bib_database.entries

  def save_to(self, dir_name):
    ensure_dir_exists(dir_name)

    data_path = os.path.join(dir_name, 'data.json')
    with open(data_path, 'w+') as json_file:
      data = {
        'projects': serialize_array(self.projects),
        'employments': serialize_array(self.employments),
        'skills': serialize_array(self.skillRecords),
        'conferences' : self.conferences,
        'total_employment': str(self.__total_employment)
      }

      self.serialize_data(data)
      json_file.write(json.dumps(data, indent=2))

    lead_path = os.path.join(dir_name, 'lead.txt')
    with open(lead_path, 'w+') as lead_file:
      lead_file.write(self.lead)
    
    sci_pubs_path = os.path.join(dir_name, 'sci_publications.bib')
    shutil.copy(self.__sci_pubs_file, sci_pubs_path)

    pop_pubs_path = os.path.join(dir_name, 'pop_publications.bib')
    shutil.copy(self.__pop_pubs_file, pop_pubs_path)

  def add_skill_experience(self, skill, period):
    logging.info('Adding period: %s -> %s' % (skill.name, period))
    skill_rec = list(x for x in self.skillRecords if x.skill == skill)[0]
    skill_rec.add_period(period)

  # Returns array [{'name' : 'skill_name', 'size' : .f_years}]
  def skills_totals(self):
    res = []
    for rec in self.skillRecords:
        res += [{'name': rec.skill.display_name(), 'size': rec.total_size(), 'attitude': rec.attitude}]
    res = (item for item in res if item['size'] > 0.0)
    return sorted(res, key=lambda rec: rec['size'], reverse=True)


  def best_skill(self):
      skills = self.skills_totals()
      return skills[0]['size']

  def has_activities(self):
    return self.popularPubs or self.scientificPubs or self.conferences

  def scopus_publication_count(self):
    return sum(is_scopus(pub) for pub in self.scientificPubs)

  def total_employment(self):
    if self.__total_employment:
      return self.__total_employment
    else:
      res = TimePeriod()
      res.startDate = self.employments[-1].period.startDate
      res.endDate = self.employments[0].period.endDate
      return res

  def remove_skill(self, skill):
    # Remove experience
    for i in range(0, len(self.skillRecords)):
      if self.skillRecords[i].skill == skill:
        del self.skillRecords[i]
        break
    
    # Remove from project tasks
    for prj in self.projects:
      prj.remove_skill(skill)

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
      logging.debug('Total scopus publications: %d' % scopus_count)

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

    ### Conferences
    self.conferences = self.conferences[0:MAX_CONFERENCES]

  def parttime_employments(self):
    return [x for x in self.employments if x.is_part_time()]

  def fulltime_employments(self):
    return [x for x in self.employments if x.is_full_time()]
