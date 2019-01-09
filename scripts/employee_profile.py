
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from basic_entities import *
import bibtexparser
import json
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding

MAX_SCI_PUBS = 4
MAX_NON_SCI_PUBS = 3
MAX_CONFERENCES = 5


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

  def load(self, input_dir):
    # Check input structure
    data_path = os.path.join(input_dir, 'data.json')
    check_always(os.path.exists(data_path), 'Primary input "%s" does not exist' % data_path)

    lead_path = os.path.join(input_dir, 'lead.txt')
    check_always(os.path.exists(lead_path), 'Lead text "%s" does not exist' % lead_path)

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
    for prj in json_node['projects']:
      new_prj = Project()
      new_prj.deserialize(prj)
      self.projects += [new_prj]

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
          log_print(LOG_LEVEL_WARNING, 'Unkown skill found: %s' % skill_name)
          skill_ref = self.skillDb.create_skill(skill_name)

        skill_rec = SkillExperience(skill_ref)
        skill_rec.attitude = skill_att
        self.skillRecords += [skill_rec]
    else:
      check_always('skills' in json_node, 'Strange JSON, where did you get it?')
      for skill_node in json_node['skills']:
        skill_ref = self.skillDb.find_skill(skill_node['name'], True)
        skill_rec = SkillExperience(skill_ref)
        skill_rec.deserialize(skill_node)

        self.skillRecords += [skill_rec]

    # Fill skill periods
    for prj in self.projects:
      # log_print(LOG_LEVEL_DEBUG, 'Adding skill periods from project: %s' % prj.name)
      # for prj_skill in prj.skills:
      #   self.add_skill_experience(prj_skill, prj.period)
        # self.skills[prj_skill].add_period(prj.period)

      for task in prj.tasks:
        for skill in task.skills:
          self.add_skill_experience(skill, task.period)

    for employment_node in json_node['employments']:
      new_empl = Employment()
      new_empl.deserialize(employment_node, self)
      self.employments += [new_empl]

    if 'conferences' in json_node:
      self.conferences = json_node['conferences']

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

  def save_to(self, dir_name):
    ensure_dir_exists(dir_name)

    data_path = os.path.join(dir_name, 'data.json')
    with open(data_path, 'w+') as json_file:
      data = {
        'projects': serialize_array(self.projects),
        'employments': serialize_array(self.employments),
        'skills': serialize_array(self.skillRecords)
      }

      self.serialize_data(data)
      json_file.write(json.dumps(data, indent=2))

    lead_path = os.path.join(dir_name, 'lead.txt')
    with open(lead_path, 'w+') as lead_file:
      lead_file.write(self.lead)

    #   data = json.load(json_data)
    #   self.deserialize(data)

  def add_skill_experience(self, skill, period):
    log_print(LOG_LEVEL_DEBUG, 'Adding period: %s -> %s' % (skill, period))
    # Find skill record for the name
    skill_rec = list(x for x in self.skillRecords if x.skill.has_synonim(skill))[0]
    skill_rec.add_period(period)
    # pass

  # Returns array [{'name' : 'skill_name', 'size' : .f_years}]
  def skills_totals(self):
    res = []
    for rec in self.skillRecords:
        res += [{'name': rec.skill.name, 'size': rec.total_size(), 'attitude': rec.attitude}]
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

    ### Conferences
    self.conferences = self.conferences[0:MAX_CONFERENCES]

