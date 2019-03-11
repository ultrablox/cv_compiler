
import os
import json
import networkx as nx
import csv
import logging
from cv import skill


class SkillsDB:
  def __init__(self):
    self.graph = nx.Graph()
    self.matchNode = skill.Skill('#matcher#')
    self.graph.add_node(self.matchNode)
    self.skills = []

  def has_skill(self, skill_name):
    res = list(x for x in self.skills if (x.name == skill_name) or x.has_synonim(skill_name))
    return len(res) > 0

  def find_skill(self, skill_name, create_if_not_exists=False):
    found_skills = list(x for x in self.skills if (x.name == skill_name) or x.has_synonim(skill_name))
    if found_skills:
      return found_skills[0]
    else:
      if create_if_not_exists:
        return self.create_skill(skill_name)
      else:
        logging.warning('Skill not found: %s' % skill_name)
        return None

  def create_skill(self, name):
    assert type(name) == str, 'Please provide string'
    
    if self.has_skill(name):
      logging.warning('Skill already exists: {}'.format(name))
      return None
    else:
      logging.info('Creating skill %s' % name)
      new_skill = skill.Skill(name)
      new_skill.set_display_name(name)
      self.skills += [new_skill]
      self.graph.add_node(new_skill)
      return new_skill

  def connect_to_matcher(self, node):
    self.graph.add_edge(node, self.matchNode, weight=0.0)

  def load_from_default_location(self):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    self.load(os.path.join(script_dir, os.pardir, os.pardir, 'database'))

  def load(self, db_dir):
    with open(os.path.join(db_dir, 'skills.json')) as f:
      skill_nodes = json.loads(f.read())

      for skill_node in skill_nodes:
        full_name = skill_node['full_name']
        new_skill = self.create_skill(full_name)
        assert new_skill, 'Skill "{}" is duplicated in DB'.format(full_name)
        if 'synonims' in skill_node:
          new_skill.synonims += skill_node['synonims']
        if 'display_name' in skill_node:
          new_skill.set_display_name(skill_node['display_name'])
        else:
          new_skill.set_display_name(full_name)

    connections = []
    with open(os.path.join(db_dir, 'skill_connections.csv'), newline='') as csvfile:
      conn_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
      for row in conn_reader:
        conn_w = (1.0 - float(row[2]))
        # print(conn_w)
        self.graph.add_edge(self.find_skill(row[0]), self.find_skill(row[1]), weight=conn_w)

  def get_relevance(self, skill_node):
    if nx.has_path(self.graph, source=self.matchNode, target=skill_node):
      p = nx.shortest_path_length(self.graph, source=self.matchNode, target=skill_node, weight='yes')
      # print('Found path:')
      # for node in p:
      #   print(str(node))
      return 1.0 / p
    else:
      return 0.0
